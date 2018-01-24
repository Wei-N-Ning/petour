
import unittest


def create_func():
    """
    No matter how many times it is called, wrapper function is the same function object
    Returns:
        int
    """
    def wrapper():
        pass

    return id(wrapper)


class Functor(object):

    def __call__(self):
        pass


def create_functor():
    return id(Functor())


class TestBasics(unittest.TestCase):

    def test_(self):
        self.assertEqual(create_func(), create_func())


if __name__ == '__main__':
    unittest.main()
