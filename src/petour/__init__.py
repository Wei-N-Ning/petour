
import sys
import weakref


# (dot-path, symbol) : (petour-obj, contextManager)
__petours = dict()


class NullContextManager(object):

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class Petour(object):

    def __init__(self, owner, func_obj, name_orig, name_backup):
        self._owner = weakref.ref(owner)
        self._func_obj = weakref.ref(func_obj)
        self.name_orig = name_orig
        self.name_backup = name_backup

    def owner(self):
        return self._owner()

    def func_obj(self):
        return self._func_obj()


def _patch_free_func(module_obj, free_function_name):
    name_backup = '{}__orig__'.format(free_function_name)
    callable_orig = getattr(module_obj, free_function_name)
    if hasattr(module_obj, name_backup):
        return

    _ = list()  # to be populated: (petour-obj, contextManager)

    def wrapper(*args, **kwargs):
        func_obj = getattr(module_obj, name_backup)
        with _[1]:
            return func_obj(*args, **kwargs)

    setattr(module_obj, name_backup, callable_orig)
    setattr(module_obj, free_function_name, wrapper)
    pt = Petour(module_obj, callable_orig, free_function_name, name_backup)
    _.append(pt)
    ctx = NullContextManager()
    _.append(ctx)
    return pt, ctx


def _patch_method(module_obj, class_dot_method):
    class_name, method_name = class_dot_method.split('.')
    name_backup = '{}__orig__'.format(method_name)
    class_obj = getattr(module_obj, class_name)
    if hasattr(class_obj, name_backup):
        return

    callable_orig = getattr(class_obj, method_name)

    _ = list()  # to be populated: (petour-obj, contextManager)

    def wrapper(*args, **kwargs):
        func_obj = getattr(class_obj, name_backup)
        with _[1]:
            return func_obj(*args, **kwargs)

    setattr(class_obj, name_backup, callable_orig)
    setattr(class_obj, method_name, wrapper)
    pt = Petour(class_obj, callable_orig, method_name, name_backup)
    _.append(pt)
    ctx = NullContextManager()
    _.append(ctx)
    return pt, ctx


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
            __petours[(module_dot_path, free_func_name)] = _patch_free_func(module_obj, free_func_name)
    if class_dot_methods:
        for class_dot_method in class_dot_methods:
            __petours[(module_dot_path, class_dot_method)] = _patch_method(module_obj, class_dot_method)


def _unpatch(pt):
    """

    Args:
        pt (Petour):

    """
    owner_obj = pt.owner()
    if owner_obj is None:
        return
    func_obj = pt.func_obj()
    if func_obj is None:
        return
    setattr(owner_obj, pt.name_orig, func_obj)
    delattr(owner_obj, pt.name_backup)


def unpatch_all():
    """
    Completely restores the patched free functions and methods, leaving no traces
    """
    for k in __petours.keys():
        pt, _ = __petours.pop(k)
        _unpatch(pt)


def petours():
    return __petours

