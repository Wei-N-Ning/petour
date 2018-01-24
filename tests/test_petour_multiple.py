
import petour

import unittest

from petourtest import sut_


class TestPatchMultipleTargets(unittest.TestCase):

    def tearDown(self):
        petour.unpatch_all()

    def test_(self):
        petour.patch('petourtest.sut_', free_func_names=['render'])
        petour.patch('petourtest.sut_', free_func_names=['compute'])
        self.assertEqual(True, sut_.render(800, 600, rate=0.5))
        self.assertAlmostEqual(3.2, sut_.compute(1.3, 3.1, mm=0.5))


if __name__ == '__main__':
    unittest.main()
