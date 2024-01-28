"""Custom Exceptions

This module contains custom error classes for :class:`matrix`. The error classes include,

- DivisionByMatrix
- MatrixDimensionsMismatch
- NotASquareMatrix
- SlicingNotAllowed
- IndexOutOfBounds
- DeterminantIsZero

Created on Oct 05 23:54:59 2023
"""


class MatrixException(Exception):
    pass


class DivisionByMatrix(MatrixException):
    def __init__(self, message="Can't divide a matrix by matrix. Invalid Operation."):
        super().__init__(message)


class MatrixDimensionsMismatch(MatrixException):
    def __init__(self, message=''):
        m = "Matrix dimensions do not match for multiplication.\n"
        super().__init__(m + message)


class NotASquareMatrix(MatrixException):
    def __init__(self, message="The provided matrix is not a square matrix.\nCan't perform LU Decomposition."):
        super().__init__(message)


class SlicingNotAllowed(MatrixException):
    def __init__(self, message="Slicing a matrix is not possible, please use integer indices."):
        super().__init__(message)


class IndexOutOfBounds(MatrixException):
    def __init__(self, message="The given index doesn't exist for the matrix."):
        super().__init__(message)


class DeterminantIsZero(MatrixException):
    def __init__(self, message="The given matrix is singular and its inverse can't be calculated."):
        super().__init__(message)
