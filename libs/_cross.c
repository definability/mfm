#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION

#include <Python.h>
#include <numpy/arrayobject.h>

#include "cross.h"

struct ModuleState {
    PyObject *error;
};

#if PY_MAJOR_VERSION >= 3
#define GETSTATE(module) ((struct ModuleState*)PyModule_GetState(module))
#else
#define GETSTATE(module) (&_state)
static struct ModuleState _state;
#endif

static PyObject* _cross (PyObject *self, PyObject *args) {
    PyObject *o_vertices=NULL, *o_triangles=NULL, *o_result=NULL;
    PyArrayObject *a_vertices=NULL, *a_triangles=NULL, *a_result=NULL;

    if (!PyArg_ParseTuple(args, "OOO!", &o_vertices, &o_triangles,
                          &PyArray_Type, &o_result)) return NULL;

    a_vertices = (PyArrayObject*)PyArray_FROM_OTF(o_vertices, NPY_FLOAT, NPY_ARRAY_IN_ARRAY);
    if (a_vertices == NULL) return NULL;
    a_triangles = (PyArrayObject*)PyArray_FROM_OTF(o_triangles, NPY_UINT16, NPY_ARRAY_IN_ARRAY);
    if (a_triangles == NULL) goto fail;
    a_result = (PyArrayObject*)PyArray_FROM_OTF(o_result, NPY_FLOAT, NPY_ARRAY_INOUT_ARRAY);
    if (a_result == NULL) goto fail;

    get_normals(PyArray_DATA(a_vertices),
                PyArray_DATA(a_triangles),
                PyArray_DATA(a_result),
                PyArray_SIZE(a_vertices) / 3,
                PyArray_SIZE(a_triangles) / 3);

    Py_DECREF(a_vertices);
    Py_DECREF(a_triangles);
    Py_DECREF(a_result);
    Py_INCREF(Py_None);
    return Py_None;

 fail:
    Py_XDECREF(a_vertices);
    Py_XDECREF(a_triangles);
    PyArray_XDECREF_ERR(a_result);
    return NULL;
}

static PyMethodDef cross_methods[] = {
    { "cross", _cross,
      METH_VARARGS,
      "Cross"},
    {NULL, NULL, 0, NULL}
};

#if PY_MAJOR_VERSION >= 3

static int cross_traverse(PyObject *m, visitproc visit, void *arg) {
    Py_VISIT(GETSTATE(m)->error);
    return 0;
}

static int cross_clear(PyObject *m) {
    Py_CLEAR(GETSTATE(m)->error);
    return 0;
}

#define INITERROR return NULL

static struct PyModuleDef cross_module = {
    PyModuleDef_HEAD_INIT,
    "cross",   /* name of module */
    "Cross module", /* module documentation, may be NULL */
    sizeof(struct ModuleState),       /* size of per-interpreter state of the module,
                or -1 if the module keeps state in global variables. */
    cross_methods,
    NULL,
    cross_traverse,
    cross_clear,
    NULL
};

PyMODINIT_FUNC PyInit_cross(void)

#else
#define INITERROR return

void initcross(void)
#endif
{
    PyObject *module;

#if PY_MAJOR_VERSION >= 3
    module = PyModule_Create(&cross_module);
#else
    module = Py_InitModule("cross", cross_methods);
#endif
    import_array();
    if (module == NULL)
        INITERROR;

    struct ModuleState *st = GETSTATE(module);

    st->error = PyErr_NewException("cross.Error", NULL, NULL);
    if (st->error == NULL) {
        Py_DECREF(module);
        INITERROR;
    }

#if PY_MAJOR_VERSION >= 3
    return module;
#endif
}
