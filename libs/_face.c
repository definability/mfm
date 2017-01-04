#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION

#include <Python.h>
#include <numpy/arrayobject.h>

#include "face.h"

struct ModuleState {
    PyObject *error;
};

static float* principal_components = NULL;
static float* pc_deviations = NULL;
static float* mean_shape = NULL;

static size_t dimensions = 0;
static size_t vertices = 0;

#if PY_MAJOR_VERSION >= 3
#define GET_STATE(module) ((struct ModuleState*)PyModule_GetState(module))
#else
#define GET_STATE(module) (&_state)
static struct ModuleState _state;
#endif

static PyObject* _init(PyObject *self, PyObject *args) {
    PyArrayObject *ao_mean_shape=NULL, *ao_principal_components=NULL,
                  *ao_pc_deviations=NULL;

    if (!PyArg_ParseTuple(args, "O!O!O!",
                          &PyArray_Type, &ao_mean_shape,
                          &PyArray_Type, &ao_principal_components,
                          &PyArray_Type, &ao_pc_deviations)) {
        return NULL;
    }

    principal_components = PyArray_DATA(ao_principal_components);
    pc_deviations = PyArray_DATA(ao_pc_deviations);
    mean_shape = PyArray_DATA(ao_mean_shape);
    dimensions = PyArray_SIZE(ao_pc_deviations);
    vertices = PyArray_SIZE(ao_mean_shape);

    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject* _calculate_face(PyObject *self, PyObject *args) {
    PyArrayObject *coefficients=NULL, *result=NULL;

    if (!PyArg_ParseTuple(args, "O!", &PyArray_Type, &coefficients)) {
        return NULL;
    }

    npy_intp* dims = malloc(sizeof(npy_intp)*2);
    dims[0] = vertices;
    dims[1] = 1;
    result = (PyArrayObject*)PyArray_ZEROS(2, dims, NPY_FLOAT, 0);

    calculate_face(
        mean_shape,
        principal_components,
        pc_deviations,
        PyArray_DATA(coefficients),
        PyArray_DATA(result),
        PyArray_SIZE(coefficients),
        dimensions,
        vertices);

    return PyArray_Return(result);
}

static PyObject* _calculate_row(PyObject *self, PyObject *args) {
    PyArrayObject *principal_components=NULL, *pc_deviations=NULL,
                  *face=NULL;
    Py_ssize_t row;
    float coefficient_difference;

    if (!PyArg_ParseTuple(args, "O!O!fnO!",
                &PyArray_Type, &principal_components,
                &PyArray_Type, &pc_deviations,
                &coefficient_difference,
                &row,
                &PyArray_Type, &face)) {
        return NULL;
    }

    calculate_row(
         PyArray_DATA(principal_components),
         PyArray_DATA(pc_deviations),
         coefficient_difference,
         row,
         PyArray_DATA(face),
         PyArray_SIZE(pc_deviations),
         PyArray_SIZE(face));

    Py_INCREF(Py_None);
    return Py_None;
}

static PyMethodDef face_methods[] = {
    { "init_face_calculator", _init,
      METH_VARARGS,
      "Cache needed data."},
    { "calculate_face", _calculate_face,
      METH_VARARGS,
      "Get array of vertices for Face."},
    { "calculate_row", _calculate_row,
      METH_VARARGS,
      "Change coefficient of one principal component in Face."},
    {NULL, NULL, 0, NULL}
};

#if PY_MAJOR_VERSION >= 3

static int face_traverse(PyObject *m, visitproc visit, void *arg) {
    Py_VISIT(GET_STATE(m)->error);
    return 0;
}

static int face_clear(PyObject *m) {
    Py_CLEAR(GET_STATE(m)->error);
    return 0;
}

#define INITERROR return NULL

static struct PyModuleDef face_module = {
    PyModuleDef_HEAD_INIT,
    "face",
    "Normal vectors processing.",
    sizeof(struct ModuleState),
    face_methods,
    NULL,
    face_traverse,
    face_clear,
    NULL
};

PyMODINIT_FUNC PyInit_face(void)

#else
#define INITERROR return

void initface(void)
#endif
{
    PyObject *module;

#if PY_MAJOR_VERSION >= 3
    module = PyModule_Create(&face_module);
#else
    module = Py_InitModule("face", face_methods);
#endif
    import_array();
    if (module == NULL) {
        INITERROR;
    }

    struct ModuleState *st = GET_STATE(module);

    st->error = PyErr_NewException("face.Error", NULL, NULL);
    if (st->error == NULL) {
        Py_DECREF(module);
        INITERROR;
    }

#if PY_MAJOR_VERSION >= 3
    return module;
#endif
}
