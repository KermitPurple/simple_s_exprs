#!/usr/bin/env python3

'''
Test cases
'''

from interpret import interpret
import unittest

class TestInterpret(unittest.TestCase):
    def test_assign(self):
        self.assertEqual(interpret('(assign x 10) x'), 10)
        self.assertEqual(interpret('(assign longer_name 6) longer_name'), 6)
        self.assertEqual(interpret('(assign slashes/too \'And strings!\') slashes/too'), 'And strings!')

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
        self.assertEqual(interpret('(mull 1 2 3 4 5 6 7 8 9 10)'), 3628800)

    def test_div(self):
        self.assertAlmostEqual(interpret('(div 2.9 2)'), 1.45)
        self.assertEqual(interpret('(div (div 3 2) 1)'), 1.5)
        self.assertEqual(interpret('(div 3 (div 2 1))'), 1.5)

if __name__ == '__main__':
    unittest.main()

