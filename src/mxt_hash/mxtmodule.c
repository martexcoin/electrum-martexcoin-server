#include <Python.h>

#include "mxt.h"

static PyObject *mxt_getpowhash(PyObject *self, PyObject *args)
{
    char *output;
    PyObject *value;
#if PY_MAJOR_VERSION >= 3
    PyBytesObject *input;
#else
    PyStringObject *input;
#endif
    if (!PyArg_ParseTuple(args, "S", &input))
        return NULL;
    Py_INCREF(input);
    output = PyMem_Malloc(32);

#if PY_MAJOR_VERSION >= 3
    mxt_hash((char *)PyBytes_AsString((PyObject*) input), output);
#else
    mxt_hash((char *)PyString_AsString((PyObject*) input), output);
#endif
    Py_DECREF(input);
#if PY_MAJOR_VERSION >= 3
    value = Py_BuildValue("y#", output, 32);
#else
    value = Py_BuildValue("s#", output, 32);
#endif
    PyMem_Free(output);
    return value;
}

static PyMethodDef MXTMethods[] = {
    { "getPoWHash", mxt_getpowhash, METH_VARARGS, "Returns the proof of work hash using mxt hash" },
    { NULL, NULL, 0, NULL }
};

#if PY_MAJOR_VERSION >= 3
static struct PyModuleDef MXTModule = {
    PyModuleDef_HEAD_INIT,
    "mxt_hash",
    "...",
    -1,
    MXTMethods
};

PyMODINIT_FUNC PyInit_mxt_hash(void) {
    return PyModule_Create(&MXTModule);
}

#else

PyMODINIT_FUNC initmxt_hash(void) {
    (void) Py_InitModule("mxt_hash", MXTMethods);
}
#endif
