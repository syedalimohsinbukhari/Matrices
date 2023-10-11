"""Created on Oct 04 21:36:44 2023"""

import numpy as np

import p_error_config as pec
from subclasses import DETERMINANT_ as DET_
from subclasses import INVERSE_ as INV_
from subclasses import MATRIX as MAT_

pec.config()


class Matrix(MAT_.MATRIX):

    def __init__(self, elements):
        super().__init__(elements)
        self.elements = elements

    def determinant(self):
        return DET_.DETERMINANT(self.n_rows, self.n_cols).determinant(self.elements)

    def inverse(self, separate_determinant=False):
        return self._give_output(INV_.INVERSE(self.elements).inverse(separate_determinant))

    def get_numpy_compatible_matrix(self):
        return np.array([i for i in self.elements])
