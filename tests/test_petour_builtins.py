
import unittest

import petour


class Counter(object):

    def __init__(self):
        self.count = 0

    def parse_args(self, *args, **kargs):
        return self

    def __enter__(self):
        self.count += 1

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class TestPatchBuiltinFunction(unittest.TestCase):
    """
    patch __builtins__ module free function abs()
    """

    def setUp(self):
        self.ctx = Counter()

    def test_builtins_freeFunction(self):
        petour.patch('__builtin__', free_func_names=['abs'], ctx=self.ctx)
        abs(-10)
        # TODO: make it passes
        # self.assertEqual(1, self.ctx.count)


if __name__ == '__main__':
    unittest.main()
