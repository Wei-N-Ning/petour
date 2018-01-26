
import ctypes
import os


def getSharedLib(fName):
    return ctypes.cdll.LoadLibrary(
        os.path.join(os.path.dirname(__file__), fName))
