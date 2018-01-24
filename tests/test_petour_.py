
import petour

import unittest

from petourtest.sut_ import foobar as __foobar
from petourtest.sut_ import FooBar
from petourtest import sut_

foobar = __foobar


class Counter(object):

    def __init__(self):
        self.count = 0

    def __enter__(self):
        self.count += 1

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class TestFreeFunction(unittest.TestCase):

    def tearDown(self):
        petour.unpatch_all()

    def test_initialState_expectNoPetourCount(self):
        self.assertFalse(petour.petours())

    def test_expectPetourCount(self):
        petour.patch('petourtest.sut_', free_func_names=['foobar'])
        self.assertEqual(1, len(petour.petours()))

    def test_unpatchAll_expectNoPetourCount(self):
        petour.patch('petourtest.sut_', free_func_names=['foobar'])
        petour.unpatch_all()
        self.assertFalse(petour.petours())

    def test_initialState_expectNoContextManagerObject(self):
        self.assertFalse(petour.petour('petourtest.sut_', 'foobar'))

    def test_expectDefaultContextManagerObject(self):
        petour.patch('petourtest.sut_', free_func_names=['foobar'])
        _, ctx = petour.petour('petourtest.sut_', 'foobar')
        self.assertTrue(ctx)

    def test_useWrongKey_expectNoContextManagerObject(self):
        petour.patch('petourtest.sut_', free_func_names=['foobar'])
        self.assertFalse(petour.petour('module.something', 'foobar'))

    def test_overrideContextManager_expectInvoked(self):
        petour.patch('petourtest.sut_', free_func_names=['foobar'])
        ctx = Counter()
        petour.set_context_manager('petourtest.sut_', 'foobar', ctx)
        foobar()
        sut_.foobar()
        self.assertEqual(2, ctx.count)

    def test_unpatchAll_expectContextManagerNotInvoked(self):
        petour.patch('petourtest.sut_', free_func_names=['foobar'])
        ctx = Counter()
        petour.unpatch_all()
        foobar()
        sut_.foobar()
        self.assertEqual(0, ctx.count)

    def test_patchTwice_expectNoSideEffect(self):
        petour.patch('petourtest.sut_', free_func_names=['foobar'])
        petour.patch('petourtest.sut_', free_func_names=['foobar'])
        self.assertEqual(1, len(petour.petours()))
        self.assertEqual(1, foobar(1))
        ctx = petour.context_manager('petourtest.sut_', 'foobar')
        self.assertTrue(ctx)
        petour.unpatch_all()
        self.assertEqual(0, len(petour.petours()))
        ctx = petour.context_manager('petourtest.sut_', 'foobar')
        self.assertFalse(ctx)


class TestClassMethods(unittest.TestCase):

    def tearDown(self):
        petour.unpatch_all()

    def test_expectPetourCount(self):
        petour.patch('petourtest.sut_', class_dot_methods=['FooBar.count'])
        self.assertEqual(1, len(petour.petours()))

    def test_unpatchAll_expectNoPetourCount(self):
        petour.patch('petourtest.sut_', class_dot_methods=['FooBar.count'])
        petour.unpatch_all()
        self.assertFalse(petour.petours())

    def test_expectDefaultContextManagerObject(self):
        petour.patch('petourtest.sut_', class_dot_methods=['FooBar.count'])
        _, ctx = petour.petour('petourtest.sut_', 'FooBar.count')
        self.assertTrue(ctx)

    def test_overrideContextManager_expectInvoked(self):
        petour.patch('petourtest.sut_', class_dot_methods=['FooBar.count'])
        ctx = Counter()
        petour.set_context_manager('petourtest.sut_', 'FooBar.count', ctx)
        FooBar().count()
        sut_.FooBar().count()
        self.assertEqual(2, ctx.count)

    def test_callPatchedInstanceMethod_expectInstanceAccessRestriction(self):
        """
        This is very important:

        A patched instance method should still be an instance method, which
        must be called from the instance not the class

        The following two test methods are to verify the access mode when
         a class-method and a static-method is patched
        """
        petour.patch('petourtest.sut_', class_dot_methods=['FooBar.count'])
        self.assertRaises(TypeError, sut_.FooBar.count)

    def test_callPatchedClassMethod_expectClassAccess(self):
        petour.patch('petourtest.sut_', class_dot_methods=['FooBar.kls_count'])
        self.assertEqual(11, sut_.FooBar.kls_count(10))

    def test_callPatchedStaticMethod_expectClassAccess(self):
        petour.patch('petourtest.sut_', class_dot_methods=['FooBar.sta_count'])
        self.assertEqual(101, sut_.FooBar.sta_count('abc'))

    def test_unpatchAll_expectContextManagerNotInvoked(self):
        petour.patch('petourtest.sut_', class_dot_methods=['FooBar.kls_count'])
        ctx = Counter()
        petour.unpatch_all()
        FooBar.kls_count(11)
        sut_.FooBar.kls_count(111)
        self.assertEqual(0, ctx.count)

    def test_patchTwice_expectNoSideEffect(self):
        petour.patch('petourtest.sut_', class_dot_methods=['FooBar.count'])
        petour.patch('petourtest.sut_', class_dot_methods=['FooBar.count'])
        self.assertEqual(1, len(petour.petours()))
        self.assertEqual(1, foobar(1))
        ctx = petour.context_manager('petourtest.sut_', 'FooBar.count')
        self.assertTrue(ctx)
        petour.unpatch_all()
        self.assertEqual(0, len(petour.petours()))
        ctx = petour.context_manager('petourtest.sut_', 'FooBar.count')
        self.assertFalse(ctx)


class TestNonCallableTypes(unittest.TestCase):
    """
    Non-callable types are not supported atm
    """

    def tearDown(self):
        petour.unpatch_all()

    def test_canNotPatchStaticVariable(self):
        petour.patch('petourtest.sut_', free_func_names=['beef'])
        self.assertFalse(petour.petours())

    def test_canNotPatchClassAttribute(self):
        petour.patch('petourtest.sut_', class_dot_methods=['FooBar.IDDQD'])
        self.assertFalse(petour.petours())


if __name__ == '__main__':
    unittest.main()
