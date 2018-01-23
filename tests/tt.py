
import dis
import copy
from types import CodeType
import types

def fix_function(func, payload):
    fn_code = func.__code__
    func.__code__ = CodeType(fn_code.co_argcount,
                             fn_code.co_kwonlyargcount,
                             fn_code.co_nlocals,
                             fn_code.co_stacksize,
                             fn_code.co_flags,
                             payload,
                             fn_code.co_consts,
                             fn_code.co_names,
                             fn_code.co_varnames,
                             fn_code.co_filename,
                             fn_code.co_name,
                             fn_code.co_firstlineno,
                             fn_code.co_lnotab,
                             fn_code.co_freevars,
                             fn_code.co_cellvars,
                             )


def foo(*args, **kwargs):
    return len(args) + len(kwargs)


class RA(object): pass


class RAII(object):

    def __init__(self):
        pass

    def __del__(self):
        pass


def bar():
    print RAII()


_ = lambda(x): None


_.func_code = copy.deepcopy(bar.func_code)


def barbar():
    print '0x1337'
    _()


bar.func_code = barbar.func_code

print 'patched'
bar()

print 'unpatched'
bar.func_code = _.func_code
del _
del barbar
bar()