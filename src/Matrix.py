"""Created on Oct 04 21:36:44 2023"""

import numpy as np

from subclasses import MATRIX as MAT_
from subclasses.specials.IDENTITY_ import IDENTITY


class Matrix(MAT_.MATRIX):

    def __init__(self, elements):
        super().__init__(elements)
        self.elements = elements

    def determinant(self):
        return super().determinant()

    def transpose(self):
        return super().transpose()

    def inverse(self, separate_determinant=False):
        return super().inverse(separate_determinant=separate_determinant)

    def get_numpy_compatible_matrix(self):
        return np.array([i for i in self.elements])

    def is_multiplicative_inverse_of(self, other):
        id_ = IDENTITY(self.n_rows).matrix()
        return True if self * other == Matrix(id_) else False
