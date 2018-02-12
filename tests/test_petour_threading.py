
import threading

import petour

import unittest

from petourtest import sut_
from petourtest.sut_ import foobar as __foobar

foobar = __foobar


class Counter(object):

    def __init__(self):
        self.count = 0

    def parse_args(self, *args, **kargs):
        return self

    def __enter__(self):
        self.count += 1

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class TestPatchStoppedThreadedFunction(unittest.TestCase):

    def tearDown(self):
        petour.unpatch_all()

    def test_patchBeforeThreadCreation(self):
        ctx = Counter()
        petour.patch('petourtest.sut_', free_func_names=['foobar'], ctx=ctx)
        t = threading.Thread(target=foobar)
        t.start()
        t.join()
        self.assertEqual(1, ctx.count)

    def test_patchAfterThreadCreation(self):
        t = threading.Thread(target=foobar)
        ctx = Counter()
        petour.patch('petourtest.sut_', free_func_names=['foobar'], ctx=ctx)
        t.start()
        t.join()
        self.assertEqual(1, ctx.count)

    def test_unpatchBeforeThreadCreation(self):
        ctx = Counter()
        petour.patch('petourtest.sut_', free_func_names=['foobar'], ctx=ctx)
        petour.unpatch_all()
        t = threading.Thread(target=foobar)
        t.start()
        t.join()
        self.assertEqual(0, ctx.count)

    def test_unpatchAfterThreadCreation(self):
        t = threading.Thread(target=foobar)
        ctx = Counter()
        petour.patch('petourtest.sut_', free_func_names=['foobar'], ctx=ctx)
        petour.unpatch_all()
        t.start()
        t.join()
        self.assertEqual(0, ctx.count)


class TestPatchRunningThreadedFunction(unittest.TestCase):

    def tearDown(self):
        petour.unpatch_all()

    def test_patchRunningThread(self):
        t = threading.Thread(target=sut_.sleep_in_loop, args=(0.05, 10))
        t.start()
        ctx = Counter()
        petour.patch('petourtest.sut_', free_func_names=['sleep_in_loop'], ctx=ctx)
        t.join()

        # the patch is not "on the train" yet
        self.assertEqual(0, ctx.count)

        t = threading.Thread(target=sut_.sleep_in_loop, args=(0.01, 10))
        t.start()
        t.join()

        # the patch is "on the train" - it is invoked
        self.assertEqual(1, ctx.count)

    def test_expectNoRacingCondition(self):
        t = threading.Thread(target=sut_.multi_foobar, args=(0.01, 50))
        t.start()
        ctx = Counter()
        petour.patch('petourtest.sut_', free_func_names=['foobar'], ctx=ctx)
        t.join()

        # during the 50 iterations, there should be at least one iteration where the detour-patch is in effect
        self.assertGreater(ctx.count, 1)


if __name__ == '__main__':
    unittest.main()
