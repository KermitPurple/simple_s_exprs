#!/usr/bin/env python3

'''
Test cases
'''

from preprocess import preprocess
from interpret import interpret
import unittest

class TestPreprocess(unittest.TestCase):
    def test_preprocess(self):
        self.assertEqual(preprocess('(add 1 2) // Comment!'), '(add 1 2) ')
        self.assertEqual(preprocess('(add 1 2)     '), '(add 1 2) ')
        self.assertEqual(preprocess('#def p (print \'test\')\np (print \'Also this!\')'), '(print \'test\') (print \'Also this!\') ')
        self.assertEqual(preprocess('#def p (print \'test\')\n (print \'just p\')'), '(print \'just p\') ')
        self.assertEqual(preprocess('#def p (print \'test\')\n (print \'just \\\' p\')'), '(print \'just \\\' p\') ')

class TestInterpret(unittest.TestCase):
    def test_assign(self):
        self.assertEqual(interpret('(assign x 10) x'), 10)
        self.assertEqual(interpret('(assign longer_name 6) longer_name'), 6)
        self.assertEqual(interpret('(assign slashes/too \'And strings!\') slashes/too'), 'And strings!')

    def test_add_assign(self):
        self.assertEqual(interpret('(assign x 10) (add_assign x 10) x'), 20)
        self.assertEqual(interpret('(assign y 2) (add_assign y 5) y'), 7)

    def test_sub_assign(self):
        self.assertEqual(interpret('(assign x 10) (add_assign x 10) x'), 20)
        self.assertEqual(interpret('(assign y 2) (add_assign y 5) y'), 7)

    def test_mul_assign(self):
        self.assertEqual(interpret('(assign x 10) (mul_assign x 10) x'), 100)
        self.assertEqual(interpret('(assign y 2) (mul_assign y 5) y'), 10)

    def test_div_assign(self):
        self.assertEqual(interpret('(assign x 10) (div_assign x 10) x'), 1)
        self.assertAlmostEqual(interpret('(assign y 2) (div_assign y 5) y'), 2 / 5)

    def test_inc(self):
        self.assertEqual(interpret('(assign x 10) (inc x) x'), 11)
        self.assertEqual(interpret('(assign y 2) (inc y) y'), 3)

    def test_dec(self):
        self.assertEqual(interpret('(assign x 10) (dec x) x'), 9)
        self.assertEqual(interpret('(assign y 2) (dec y) y'), 1)

    def test_neg(self):
        self.assertEqual(interpret('(neg 3.5)'), -3.5)
        self.assertEqual(interpret('(neg 5)'), -5)

    def test_add(self):
        self.assertAlmostEqual(interpret('(add 2.1 2)'), 4.1)
        self.assertEqual(interpret('(add 1 (add 2 3))'), 6)
        self.assertEqual(interpret('(add (add 1 2) 3)'), 6)
        self.assertEqual(interpret('(add 1 2 3 4 5 6 7 8 9 10)'), 55)

    def test_sub(self):
        self.assertAlmostEqual(interpret('(sub 2.9 2)'), 0.9)
        self.assertEqual(interpret('(sub (sub 3 2) 1)'), 0)
        self.assertEqual(interpret('(sub 3 (sub 2 1))'), 2)

    def test_mul(self):
        self.assertAlmostEqual(interpret('(mul 2.9 2)'), 5.8)
        self.assertEqual(interpret('(mul (mul 3 2) 1)'), 6)
        self.assertEqual(interpret('(mul 3 (mul 2 1))'), 6)
        self.assertEqual(interpret('(mul 1 2 3 4 5 6 7 8 9 10)'), 3628800)

    def test_div(self):
        self.assertAlmostEqual(interpret('(div 2.9 2)'), 1.45)
        self.assertEqual(interpret('(div (div 3 2) 1)'), 1.5)
        self.assertEqual(interpret('(div 3 (div 2 1))'), 1.5)

    def test_mod(self):
        self.assertAlmostEqual(interpret('(mod 2.9 2)'), 0.9)
        self.assertEqual(interpret('(mod (mod 3 2) 2)'), 1)
        self.assertEqual(interpret('(mod 3 (mod 5 3))'), 1)

    def test_eq(self):
        self.assertTrue(interpret('(eq 0 0)'))
        self.assertTrue(interpret('(eq 1 1)'))
        self.assertTrue(interpret('(eq 10 10)'))
        self.assertFalse(interpret('(eq 0 1)'))

    def test_lt(self):
        self.assertFalse(interpret('(lt 0 0)'))
        self.assertFalse(interpret('(lt 2 1)'))
        self.assertTrue(interpret('(lt 9 10)'))
        self.assertTrue(interpret('(lt 0 1)'))

    def test_gt(self):
        self.assertFalse(interpret('(gt 0 0)'))
        self.assertTrue(interpret('(gt 2 1)'))
        self.assertFalse(interpret('(gt 9 10)'))
        self.assertFalse(interpret('(gt 0 1)'))

    def test_le(self):
        self.assertTrue(interpret('(le 0 0)'))
        self.assertFalse(interpret('(le 2 1)'))
        self.assertTrue(interpret('(le 9 10)'))
        self.assertTrue(interpret('(le 0 1)'))

    def test_ge(self):
        self.assertTrue(interpret('(ge 0 0)'))
        self.assertTrue(interpret('(ge 2 1)'))
        self.assertFalse(interpret('(ge 9 10)'))
        self.assertFalse(interpret('(ge 0 1)'))

    def test_func(self):
        self.assertEqual(interpret('(def square (x) (* x x)) (square 4)'), 16)
        self.assertEqual(interpret('(def f () (= x 10)) (f) x'), None)

if __name__ == '__main__':
    unittest.main()

