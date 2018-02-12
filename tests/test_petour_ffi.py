
import petour
import petourtest

import unittest


class TestPatchFFIFunction(unittest.TestCase):

    def setUp(self):
        self.m = petourtest.getSharedLib('sut_ffi.so')

    def tearDown(self):
        petour.unpatch_all()

    def test_(self):
        self.m.foobar_iff = None


if __name__ == '__main__':
    unittest.main()
