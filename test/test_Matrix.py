"""Created on Oct 08 21:27:22 2023"""
from unittest import TestCase

from Matrix import Matrix


class TestMatrix(TestCase):
    a = Matrix([[2, 3], [-5, 6]])
    b = Matrix([[2, 0], [3, 5]])
    c = Matrix([[4], [0], [6]])

    d = Matrix([3])
    e = Matrix([5 - 2])

    f = Matrix([[3 - 1], [3 + 3]])
    g = Matrix([[2], [6]])

    h = Matrix([[2, 6], [3, 2]])
    i = Matrix([[1, -5], [2, 3]])

    j = Matrix([[0], [1], [2]])
    k = Matrix([[1, 2], [3, 4]])
    l_ = Matrix([[1, 2], [2, -1], [3, 0]])

    m = Matrix([[2, 1], [-1, 3]])
    n = Matrix([[3], [1]])
    o = Matrix([[-1, 0], [1, 2]])

    p = Matrix([[-1, 2], [2, 1]])
    q = Matrix([[1], [-1]])

    r1 = Matrix([[1, 2, 3], [-1, -1, -1], [0, 1, 2]])
    r2 = Matrix([[1, 1, 1], [2, 2, 2], [3, 3, 3]])
    r3 = Matrix([[1, 0], [0, 1]])
    r4 = Matrix([[0, 2], [3, 0]])
    r5 = Matrix([[1, 1], [1, 0]])

    s1 = Matrix([[1, -2], [3, 4]])
    s2 = Matrix([[0, 7], [-3, 8]])

    def test_order(self):
        self.assertEqual(self.a.dim, 'RxC: 2x2')
        self.assertEqual(self.b.dim, 'RxC: 2x2')
        self.assertEqual(self.c.dim, 'RxC: 3x1')

    def test_equal(self):
        self.assertTrue(self.d == self.e)
        self.assertTrue(self.f == self.g)
        self.assertFalse(self.d == self.g)

    def test_negation(self):
        self.assertEqual(-self.h, Matrix([[-2, -6], [-3, -2]]))
        self.assertEqual(-self.i, Matrix([[-1, 5], [-2, -3]]))

    def test_transpose(self):
        self.assertEqual(self.j.transpose(), Matrix([0, 1, 2]))
        self.assertEqual(self.k.transpose(), Matrix([[1, 3], [2, 4]]))
        # transpose of transpose is the matrix itself
        self.assertTrue(self.k.transpose().transpose() == self.k)
        self.assertEqual(self.l_.transpose(), Matrix([[1, 2, 3], [2, -1, 0]]))
        self.assertEqual((self.s1 - self.s2).transpose(), self.s1.transpose() - self.s2.transpose())

    def test_addition(self):
        self.assertEqual(self.m + self.o, Matrix([[1, 1], [0, 5]]))
        self.assertEqual(self.r1 + self.r2, Matrix([[2, 3, 4], [1, 1, 1], [3, 4, 5]]))
        self.assertEqual((self.r3 + self.r4) + self.r5, Matrix([[2, 3], [4, 1]]))

    def test_multiplication(self):
        self.assertEqual(2 * self.p, Matrix([[-2, 4], [4, 2]]))
        self.assertEqual(-1 * self.q, Matrix([[-1], [1]]))
        self.assertEqual(3 * self.s1 - 2 * self.s2, Matrix([[3, -20], [15, -4]]))
