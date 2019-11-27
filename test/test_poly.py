import unittest

from ntru.Poly import PolyRingModP, DTYPE
import numpy as np


class TestPoly(unittest.TestCase):

    def test_mul(self):
        poly1 = PolyRingModP(3, 2, [1, 0, 1])
        poly2 = PolyRingModP(3, 2, [1, 0, 2])
        self.assertEqual(poly1.N, poly2.N)
        self.assertEqual(poly1.p, poly2.p)
        c = poly1 * poly2
        self.assertEqual(c.N, poly1.N)
        self.assertEqual(c.p, poly1.p)
        self.assertTrue(all(c.coefs == [1, 2, 3]))
        self.assertTrue(all((poly1*10).coefs == [10, 0, 10]))
        self.assertTrue(all((10*poly1).coefs == [10, 0, 10]))

    def test_mod_p(self):
        poly1 = PolyRingModP(3, 2, [1, 0, 1])
        poly2 = PolyRingModP(3, 2, [1, 0, 2])
        c = poly1 * poly2
        c.mod_p()
        self.assertTrue(all(poly1.coefs == [1, 0, 1]))

    def test_fast_mul(self):
        poly1 = PolyRingModP(100, 2)
        poly2 = PolyRingModP(100, 2)
        poly1.random_poly(10)
        poly2.random_poly(10)
        self.assertEqual(poly1.N, poly2.N)
        self.assertEqual(poly1.p, poly2.p)
        c = poly1.fast_mul(poly2)
        self.assertEqual(c.N, poly1.N)
        self.assertEqual(c.p, poly1.p)
        self.assertTrue(all(c.coefs == (poly1*poly2).coefs))
        self.assertTrue(all(poly1.fast_mul(10).coefs == (poly1*10).coefs))

    def test_add(self):
        poly1 = PolyRingModP(3, 2, [1, 0, 1])
        poly2 = PolyRingModP(3, 2, [2, 0])
        self.assertTrue(all((poly1+1).coefs==[2, 0, 1]))
        self.assertTrue(all((poly1+2).coefs==[3, 0, 1]))
        self.assertTrue(all((poly1+poly2).coefs==[3, 0, 1]))

    def test_sub(self):
        poly1 = PolyRingModP(3, 2, [1, 0, 1])
        poly2 = PolyRingModP(3, 2, [2, 0, 2])
        self.assertTrue(all((poly1-1).coefs==[0, 0, 1]))
        self.assertTrue(all((poly1-2).coefs==[-1, 0, 1]))
        self.assertTrue(all((poly1-poly2).coefs==[-1, 0, -1]))

    def test_get_degree(self):
        poly1 = PolyRingModP(4, 2, [1, 0, 1, 0, 0])
        poly2 = PolyRingModP(4, 2, [1, 0, 1, 1])
        self.assertEqual(PolyRingModP.get_degree(poly1.coefs), 2)
        self.assertEqual(PolyRingModP.get_degree(poly2.coefs), 3)

    def test_div(self):
        poly1 = np.array([1, 0, 0, 2], dtype=DTYPE)
        poly2 = np.array([0, 1, 1], dtype=DTYPE)
        q, r = PolyRingModP.div(3, poly1, poly2)
        self.assertTrue(all(q==[1, 2]))
        self.assertTrue(all(r==[1, 2]))
        poly1 = np.array([1, 0, 1, 1, 1], dtype=DTYPE)
        poly2 = np.array([1, 1], dtype=DTYPE)
        q, r = PolyRingModP.div(2, poly1, poly2)
        self.assertTrue(all(q==[1, 1, 0, 1]))
        self.assertTrue(all(r==[0]))
        poly1 = np.array([-1, 0, 0, 1], dtype=DTYPE)
        poly2 = np.array([2, 2], dtype=DTYPE)
        q, r = PolyRingModP.div(3, poly1, poly2)
        self.assertTrue(all(q==[2, 1, 2]))
        self.assertTrue(all(r==[1]))

    # bug
    def test_eea(self):
        poly1 = np.array([-1, 0, 0, 1], dtype=DTYPE)
        poly2 = np.array([1, 0, 1], dtype=DTYPE)
        u, v, d = PolyRingModP.extended_euclidean_algorithm(3, poly1, poly2)
        self.assertTrue(all(u==[2, 1]))
        self.assertTrue(all(v==[1, 1, 2]))
        self.assertTrue(all(d==[2]))

        u, v, d = PolyRingModP.extended_euclidean_algorithm(2, poly1, poly2)
        conv1 = PolyRingModP.remove_right_zeros((np.convolve(u, poly1) + np.convolve(v, poly2)) % 2)
        self.assertTrue(all(conv1 == d))

    def test_inv_mod_p(self):
        poly2 = np.array([1, 0, 1], dtype=DTYPE)
        c = PolyRingModP(3, 3, poly2) * PolyRingModP(3, 3, PolyRingModP.inverse_mod_p(3, 3, poly2))
        self.assertTrue(all(PolyRingModP.remove_right_zeros(c.coefs % 3) == [1]))
        poly1 = np.zeros(100, dtype=DTYPE)
        poly1[2] = 1
        poly1[5] = 2
        poly1[7] = 5
        tmp = PolyRingModP(401, 3, PolyRingModP.inverse_mod_p(401, 3, poly1))
        c = PolyRingModP(401, 3, poly1) * tmp
        self.assertTrue(all(PolyRingModP.remove_right_zeros(c.coefs % 3) == [1]))

    def test_inv_mod_p_e(self):
        poly2 = np.array([0, 1], dtype=DTYPE)
        tmp = PolyRingModP.inverse_mod_p_e(3, 2, poly2, 11)
        c = PolyRingModP(3, 2**11, poly2) * PolyRingModP(3, 2**11, tmp)
        self.assertTrue(all(PolyRingModP.remove_right_zeros(c.coefs % 2**11) == [1]))
        poly1 = np.array(range(115), dtype=DTYPE) % 2
        tmp = PolyRingModP.inverse_mod_p_e(401, 2, poly1, 11)
        c = PolyRingModP.mul(401, poly1, tmp) % (2 ** 11)
        self.assertTrue(all(PolyRingModP.remove_right_zeros(c) == [1]))

    def test_static_mul(self):
        poly1 = np.array([1, 2, 3], dtype=DTYPE)
        poly2 = np.array([1, 1], dtype=DTYPE)
        c = PolyRingModP.mul(3, poly1, poly2)
        self.assertTrue(all(PolyRingModP.remove_right_zeros(c%3) == [1, 0, 2]))

    def test_product_mul(self):
        poly1 = PolyRingModP(8, 2)
        poly2 = PolyRingModP(8, 2)
        poly3 = PolyRingModP(8, 2)
        poly1.random_poly(2)
        poly2.random_poly(3)
        poly3.random_poly(1)
        c1 = poly1 * poly2 + poly3
        c2 = PolyRingModP.product_mul(poly1, poly2, poly3)
        self.assertTrue(all(c1.coefs==c2.coefs))

if __name__ == '__main__':
    unittest.main()

