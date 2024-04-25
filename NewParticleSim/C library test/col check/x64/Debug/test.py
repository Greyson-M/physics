import ctypes
import numpy as np

# Load the shared library into c types.
lib = ctypes.CDLL('D:/Documents/programming/physics/NewParticleSim/C library test/col check/x64/Debug/col check.dll')
lib.distance.argtypes = [ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float]
lib.distance.restype = ctypes.c_float

lib.add.argtypes = [ctypes.c_int, ctypes.c_int]
lib.add.restype = ctypes.c_int

class Vector(ctypes.Structure):
    _fields_ = [("x", ctypes.c_float), ("y", ctypes.c_float)]

lib.check.argtypes = [ctypes.POINTER(Vector), ctypes.c_int, ctypes.c_int]
lib.check.restype = ctypes.c_int

def check():
    v1 = Vector()
    v1.x = 70
    v1.y = 10
    v2 = Vector()
    v2.x = 3
    v2.y = 4
    v3 = Vector()
    v3.x = 3
    v3.y = 4

    arr = [v1, v2, v3]
    size = len(arr)
    arr = (Vector * len(arr))(*arr)
    arr = ctypes.cast(arr, ctypes.POINTER(Vector))

    c = lib.check(arr, 0, size)

    return c

print (check())
