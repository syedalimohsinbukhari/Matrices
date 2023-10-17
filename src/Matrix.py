"""Created on Oct 04 21:36:44 2023"""

from subclasses import MATRIX as MAT_
from subclasses.specials.IDENTITY_ import IDENTITY


class Matrix(MAT_.MATRIX):

    def __init__(self, elements):
        super().__init__(elements)
        self.elements = elements

    def determinant(self):
        return super().determinant()

    def inverse(self):
        return super().inverse()

    def transpose(self):
        return super().transpose()

    def get_numpy_compatible_matrix(self, array_function):
        return array_function([i for i in self.elements])

    def is_multiplicative_inverse_of(self, other):
        id_ = IDENTITY(self.n_rows).matrix()
        return True if self * other == Matrix(id_) else False
