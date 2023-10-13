"""Created on Oct 04 21:36:44 2023"""

import numpy as np

import p_error_config as pec
from subclasses import DETERMINANT_ as DET_
from subclasses import MATRIX as MAT_
from subclasses.specials.IDENTITY_ import IDENTITY

pec.config()


class Matrix(MAT_.MATRIX):

    def __init__(self, elements):
        super().__init__(elements)
        self.elements = elements

    def determinant(self):
        return DET_.DETERMINANT(self.n_rows, self.n_cols).determinant(self.elements)

    def transpose(self):
        return super().transpose()

    def inverse(self, separate_determinant=False):
        return super().inverse(separate_determinant)

    def get_numpy_compatible_matrix(self):
        return np.array([i for i in self.elements])

    def is_multiplicative_inverse(self, other):
        id_ = IDENTITY(self.n_rows).matrix()
        return True if self * other == Matrix(id_) else False
