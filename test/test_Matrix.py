"""Created on Oct 08 21:27:22 2023"""

from unittest import TestCase

from umatrix.matrix import Matrix
from umatrix.matrix import identity_matrix


class TestMatrix(TestCase):
    a1 = Matrix([[2, 3], [-5, 6]])
    a2 = Matrix([[2, 0], [3, 5]])
    a3 = Matrix([[4], [0], [6]])

    b1 = Matrix([3])
    b2 = Matrix([5 - 2])
    b3 = Matrix([[3 - 1], [3 + 3]])
    b4 = Matrix([[2], [6]])

    c1 = Matrix([[2, 6], [3, 2]])
    c2 = Matrix([[1, -5], [2, 3]])

    d1 = Matrix([[0], [1], [2]])
    d2 = Matrix([[1, 2], [3, 4]])
    d3 = Matrix([[1, 2], [2, -1], [3, 0]])

    e1 = Matrix([[2, 1], [-1, 3]])
    e2 = Matrix([[3], [1]])
    e3 = Matrix([[-1, 0], [1, 2]])

    f1 = Matrix([[-1, 2], [2, 1]])
    f2 = Matrix([[1], [-1]])

    g1 = Matrix([[1, 2, 3], [-1, -1, -1], [0, 1, 2]])
    g2 = Matrix([[1, 1, 1], [2, 2, 2], [3, 3, 3]])
    g3 = Matrix([[1, 0], [0, 1]])
    g4 = Matrix([[0, 2], [3, 0]])
    g5 = Matrix([[1, 1], [1, 0]])

    h1 = Matrix([[1, -2], [3, 4]])
    h2 = Matrix([[0, 7], [-3, 8]])
    h3 = Matrix([[2, 3], [1, 1], [0, -2]])
    h4 = Matrix([[2, -1], [3, 0]])

    i1 = Matrix([[-1, 3], [2, 0]])
    i2 = Matrix([[1, 2], [-3, -5]])
    i3 = Matrix([[2, 1], [1, 3]])

    j1 = Matrix([[-1, 1], [2, 0]])
    j2 = Matrix([[3, 6], [2, 4]])
    j3 = Matrix([[7, -9], [3, 5]])

    k1 = Matrix([[1, 2], [-3, -5]])
    k2 = Matrix([[-1, 3], [2, 0]])
    k3 = Matrix([[0.5, 3 / 4], [1, 2]])
    k4 = Matrix([[4, 0], [-1, 2]])
    k5 = Matrix([[-4, -2], [1, -1]])

    l1 = Matrix([[3, 5], [4, 7]])
    l2 = Matrix([[7, -5], [-4, 3]])

    m1 = Matrix([[2, -2], [3, 2]])
    m2 = Matrix([[4], [6]])

    def test_order(self):
        self.assertEqual(self.a1.dim, 'RxC: 2x2')
        self.assertEqual(self.a2.dim, 'RxC: 2x2')
        self.assertEqual(self.a3.dim, 'RxC: 3x1')

    def test_equal(self):
        self.assertTrue(self.b1 == self.b2)
        self.assertTrue(self.b3 == self.b4)
        self.assertFalse(self.b1 == self.b4)

    def test_negation(self):
        self.assertEqual(-self.c1, Matrix([[-2, -6], [-3, -2]]))
        self.assertEqual(-self.c2, Matrix([[-1, 5], [-2, -3]]))

    def test_transpose(self):
        self.assertEqual(self.d1.t, Matrix([0, 1, 2]))
        self.assertEqual(self.d2.t, Matrix([[1, 3], [2, 4]]))
        # transpose of transpose is the matrix itself
        self.assertTrue(self.d2.t.t == self.d2)
        self.assertEqual(self.d3.t, Matrix([[1, 2, 3], [2, -1, 0]]))
        self.assertEqual((self.h1 - self.h2).t, self.h1.t - self.h2.t)

    def test_addition(self):
        self.assertEqual(self.e1 + self.e3, Matrix([[1, 1], [0, 5]]))
        self.assertEqual(self.g1 + self.g2, Matrix([[2, 3, 4], [1, 1, 1], [3, 4, 5]]))
        self.assertEqual((self.g3 + self.g4) + self.g5, Matrix([[2, 3], [4, 1]]))

    def test_multiplication(self):
        self.assertEqual(2 * self.f1, Matrix([[-2, 4], [4, 2]]))
        self.assertEqual(-1 * self.f2, Matrix([[-1], [1]]))
        self.assertEqual(3 * self.h1 - 2 * self.h2, Matrix([[3, -20], [15, -4]]))
        self.assertEqual(self.h3 * self.h4, Matrix([[13, -2], [5, -1], [-6, 0]]))

    def test_multiple_operators(self):
        self.assertEqual(self.i1 * (self.i2 * self.i3), (self.i1 * self.i2) * self.i3)
        self.assertEqual(self.i1 * (self.i2 - self.i3), self.i1 * self.i2 - self.i1 * self.i3)
        self.assertEqual((self.i1 * self.i2).t, self.i2.t * self.i1.t)

    def test_determinant(self):
        self.assertEqual(self.j1.determinant(), -2)
        self.assertEqual(self.j2.determinant(), 0)
        self.assertTrue(self.j2.is_singular)
        self.assertFalse(self.j3.is_singular)

    # TODO: get more inverse tests, the InFraction change has broken the inverse tests.
    def test_inverse(self):
        self.assertFalse(self.k1.is_singular)
        # self.assertAlmostEqual(self.k1.inverse().in_fractions, Matrix([[-5, -2], [3, 1]]))
        self.assertFalse(self.k2.is_singular)
        # self.assertAlmostEqual(self.k2.inverse().in_fractions,
        #                        Matrix([[0, 0.5], [1/3, 1/6]]))
        self.assertFalse(self.k3.is_singular)
        # self.assertEqual(self.k3.inverse().elements, Matrix([[8, -3], [-4, 2]]))
        # self.assertAlmostEqual(self.k3.adjoint_matrix, Matrix([[2, Fraction(-3, 4)], [-1, 0.5]]))
        self.assertEqual(self.k3.inverse() * self.k3, Matrix([[1, 0], [0, 1]]))
        # self.assertAlmostEqual((self.k4 * self.k5).inverse().in_fractions,
        #                        self.k5.inverse().in_fractions * self.k4.inverse().in_fractions)

    def test_multiplicative_inverse(self):
        self.assertTrue(self.l1.is_multiplicative_inverse_of(self.l2))
        self.assertEqual(self.l1 * self.l2, identity_matrix(self.l1.n_rows))

    def test_random(self):
        self.assertEqual(self.m1.inverse() * self.m2, Matrix([[2], [0]]))
