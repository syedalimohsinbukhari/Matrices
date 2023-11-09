"""Created on Oct 04 21:36:44 2023"""

from subclasses import MatrixBaseClass as MAT_
from subclasses.EXCEPTIONS_ import MatrixDimensionsMismatch
from subclasses.MatrixBaseClass import IdentityMatrix


class Matrix(MAT_.MatrixBaseClass):

    def __init__(self, elements):
        super().__init__(elements)

    @staticmethod
    def _give_output(output):
        return Matrix(output)

    def _identity_matrix(self):
        return IdentityMatrix(self.n_rows).identity()

    def get_numpy_compatible_matrix(self, array_function):
        return array_function([i for i in self.elements])

    def is_multiplicative_inverse_of(self, other):
        return True if self * other == self._identity_matrix() else False

    def is_symmetric(self):
        return True if self == self.transpose() else False

    def is_orthogonal(self):
        return True if self * self.transpose() == self._identity_matrix() else False

    def is_orthogonal_to(self, other):
        if self.dim != other.dim:
            raise MatrixDimensionsMismatch()
        return True if self * other.transpose() == self._identity_matrix() else False
