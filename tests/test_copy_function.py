

import petour

import unittest


def fo():
    return 'fo'


def mo():
    return 'mo'


class TestCopyFunction(unittest.TestCase):

    def test_ensureDeepCopy(self):
        _ = petour.copy_func(fo)
        __ = lambda: 'yo'
        fo.__code__ = __.__code__
        self.assertEqual('yo', fo())
        self.assertEqual('fo', _())


if __name__ == '__main__':
    unittest.main()
