
import copy
import sys
import types
import weakref


# (dot-path, symbol) : (petour-obj, contextManager)
__petours = dict()
__mapping = dict()


class NullContextManager(object):

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class Petour(object):

    def __init__(self, owner, func_obj, name_orig, name_backup):
        self._owner = owner
        self._func_obj = weakref.ref(func_obj)
        self.name_orig = name_orig
        self.name_backup = name_backup

    def owner(self):
        return self._owner

    def func_obj(self):
        return self._func_obj()


def get_callable(codeObj):
    return __mapping[codeObj]


def _patch_free_func(module_obj, free_function_name):
    name_backup = '{}__orig__'.format(free_function_name)
    callable_orig = getattr(module_obj, free_function_name)
    if hasattr(module_obj, name_backup):
        return

    __ = lambda(x): None
    __.__code__ = copy.deepcopy(callable_orig.func_code)
    setattr(module_obj, name_backup, __)

    def wrapper(*args, **kwargs):
        import sys
        import inspect
        fr = inspect.currentframe()
        pt, ctx = sys.modules['petour'].get_callable(fr.f_code)
        f = pt.func_obj()
        with ctx:
            return f(*args, **kwargs)

    callable_orig.__code__ = wrapper.func_code

    pt = Petour(module_obj, __, free_function_name, name_backup)
    ctx = NullContextManager()
    record = [pt, ctx]
    __mapping[wrapper.__code__] = record
    return record


def _patch_method(module_obj, class_dot_method):
    class_name, method_name = class_dot_method.split('.')
    name_backup = '{}__orig__'.format(method_name)
    class_obj = getattr(module_obj, class_name)
    method_obj = getattr(class_obj, method_name)
    if not isinstance(method_obj, types.UnboundMethodType):
        return

    callable_obj = method_obj.im_func

    if hasattr(class_obj, name_backup):
        return

    __ = lambda(x): None
    __.__code__ = copy.deepcopy(callable_obj.__code__)
    setattr(class_obj, name_backup, __)

    def wrapper(*args, **kwargs):
        import sys
        import inspect
        fr = inspect.currentframe()
        pt, ctx = sys.modules['petour'].get_callable(fr.f_code)
        f = pt.func_obj()
        with ctx:
            return f(*args, **kwargs)

    callable_obj.__code__ = wrapper.__code__

    pt = Petour(class_obj, __, method_name, name_backup)
    ctx = NullContextManager()
    record = [pt, ctx]
    __mapping[wrapper.__code__] = record
    return record


def patch(module_dot_path, free_func_names=None, class_dot_methods=None):
    """
    Use this function to monkey-patch a free-function or method, adding
    a profiler hook to it.

    The free functions and methods are passed in by names,

    moduleDotPath examples:
    'corelib.publish'

    free function examples:
    ['exists', 'send_all', 'publish']

    method examples (using class.method format):
    ['Factory.create', 'Graph.addNode']

    Args:
        module_dot_path (str):
        free_func_names (list):
        class_dot_methods (list):

    """

    module_obj = sys.modules.get(module_dot_path)
    if module_obj is None:
        module_obj = __import__(module_dot_path, fromlist=[''])
    if free_func_names:
        for free_func_name in free_func_names:
            r = _patch_free_func(module_obj, free_func_name)
            if r:
                __petours[(module_dot_path, free_func_name)] = r
    if class_dot_methods:
        for class_dot_method in class_dot_methods:
            r = _patch_method(module_obj, class_dot_method)
            if r:
                __petours[(module_dot_path, class_dot_method)] = r


def _unpatch(pt):
    """

    Args:
        pt (Petour):

    """
    owner_obj = pt.owner()
    if owner_obj is None:
        return
    func_obj = pt.func_obj()  # __
    if func_obj is None:
        return
    f = getattr(owner_obj, pt.name_orig)
    if isinstance(f, types.UnboundMethodType):
        f.im_func.__code__ = func_obj.__code__
    else:
        f.__code__ = func_obj.__code__
    delattr(owner_obj, pt.name_backup)


def unpatch_all():
    """
    Completely restores the patched free functions and methods, leaving no traces
    """
    for k in __petours:
        pt, _ = __petours[k]
        _unpatch(pt)
    __petours.clear()
    __mapping.clear()


def petours():
    return __petours


def petour(dot_path, symbol):
    return __petours.get((dot_path, symbol))


def context_manager(dot_path, symbol):
    return __petours.get((dot_path, symbol), (None, None))[1]


def set_context_manager(dot_path, symbol, ctx):
    r = __petours.get((dot_path, symbol))
    if r is not None:
        r[1] = ctx
