#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION

#include <Python.h>
#include <numpy/arrayobject.h>

#include "normals.h"

struct ModuleState {
    PyObject *error;
};

#if PY_MAJOR_VERSION >= 3
#define GET_STATE(module) ((struct ModuleState*)PyModule_GetState(module))
#else
#define GET_STATE(module) (&_state)
static struct ModuleState _state;
#endif

static PyObject* _normals (PyObject *self, PyObject *args) {
    PyArrayObject *vertices=NULL, *triangles=NULL, *result=NULL;

    if (!PyArg_ParseTuple(args, "O!O!",
                          &PyArray_Type, &vertices,
                          &PyArray_Type, &triangles)) {
        return NULL;
    }

    result = (PyArrayObject*)PyArray_NewLikeArray(
        vertices, NPY_KEEPORDER, NULL, 1);

    if (!result) {
        return NULL;
    }

    PyArray_FILLWBYTE(result, 0);
    // memset((void*)PyArray_DATA(result), 0,
    //        PyArray_SIZE(result) * sizeof(float));


    get_normals(PyArray_DATA(vertices),
                PyArray_DATA(triangles),
                PyArray_DATA(result),
                PyArray_SIZE(vertices) / 3,
                PyArray_SIZE(triangles) / 3);

    return PyArray_Return(result);
}

static PyMethodDef normals_methods[] = {
    { "get_normals", _normals,
      METH_VARARGS,
      "Get normalized normal vectors for each vertex.\n\n"
      "Normal vector of each vertex is average normal vector\n"
      "of triangles connected by this vertex."},
    {NULL, NULL, 0, NULL}
};

#if PY_MAJOR_VERSION >= 3

static int normals_traverse(PyObject *m, visitproc visit, void *arg) {
    Py_VISIT(GET_STATE(m)->error);
    return 0;
}

static int normals_clear(PyObject *m) {
    Py_CLEAR(GET_STATE(m)->error);
    return 0;
}

#define INITERROR return NULL

static struct PyModuleDef normals_module = {
    PyModuleDef_HEAD_INIT,
    "normals",
    "Normal vectors processing.",
    sizeof(struct ModuleState),
    normals_methods,
    NULL,
    normals_traverse,
    normals_clear,
    NULL
};

PyMODINIT_FUNC PyInit_normals(void)

#else
#define INITERROR return

void initnormals(void)
#endif
{
    PyObject *module;

#if PY_MAJOR_VERSION >= 3
    module = PyModule_Create(&normals_module);
#else
    module = Py_InitModule("normals", normals_methods);
#endif
    import_array();
    if (module == NULL) {
        INITERROR;
    }

    struct ModuleState *st = GET_STATE(module);

    st->error = PyErr_NewException("normals.Error", NULL, NULL);
    if (st->error == NULL) {
        Py_DECREF(module);
        INITERROR;
    }

#if PY_MAJOR_VERSION >= 3
    return module;
#endif
}
