"""Matrix base module

This module provides functionality to create matrices and perform various operations on them. The base class is,

- :class:`matrix`

which gives the functionality of generating the matrices. All the matrices have the following associated properties,

- n_rows: Number of rows of the matrix.
- n_cols: Number of columns of the matrix.
- dim: String describing the dimensions of the matrix.
- is_square: Whether the given matrix is square or not, e.g., has equal number of rows and columns.
- is_singular: Whether the given matrix is singular or not, e.g., det(Matrix) = 0 or not.
- trace: The trace of the matrix.
- in_fractions: Gives the output of the matrix in fractions.
- t: Short form for transpose of the matrix.
- transpose: Transpose of the matrix.

Along with these properties, the matrix object has the following functions,

- is_symmetric: Whether the matrix is symmetric or not.
- is_orthogonal: Whether the matrix is orthogonal or not.
- is_positive_definite: Whether the matrix is positive definite or not.
- determinant: The determinant of the matrix.
- inverse: The inverse of the matrix.
- adjoint_matrix: The adjoint of the matrix.
- diagonal: The diagonal elements of the matrix as a vector.
- diagonal_of_matrix: The diagonal elements of the matrix in a square matrix.
- hadamard_product: Performs element wise multiplication for two given matrices.
- elementwise_product: Same as hadamard_product.
- is_multiplicative_inverse_of: Whether the self matrix is a multiplicative inverse of the other matrix or not.
- is_orthogonal_to: Whether the self matrix is orthogonal to another matrix or not.
- get_numpy_compatible_matrix: Gives the numpy compatible matrix.
- dot: Dot product of two matrices.

Additionally, the module provides the following functions,

- determinant: Calculate the determinant of the given matrix.
- identity_matrix: Generates identity matrix for given rows and columns.
- null_matrix: Generates null matrix for given rows and columns.
- vector_mag: Gives the magnitude of the given vector.
- matrix_copy: Makes a deepcopy of matrix to avoid destructive manipulation of the original matrix.
- map_to_matrix: Provides an interface to map a function to the matrix, fully, diagonally or off-diagonally.

And two classes,

- InFractions: Provides functionality to turn matrices from decimal to fractions.
- Inverse: Class for calculation of inverse of the given matrix.

Created on Oct 07 17:48:12 2023
"""

from copy import deepcopy
from fractions import Fraction
from itertools import chain
from math import sqrt

from . import IFloat, LList, OptIFloat
from .__backend import custom_exceptions_ as c_ex_


# TODO: Check the setting of values inside column matrices, they're acting up

class Matrix:

    def __init__(self, elements, n_decimal=-1):
        self.elements = elements
        self.n_decimal = n_decimal

    def __repr__(self):
        elements = self.elements

        out = ''
        if self.n_rows == 1:
            max_width = max(len(str(row)) for row in elements)
            out += '[' + ' '.join([str(element).rjust(max_width) for element in elements]) + ']'
        else:
            out = '['
            max_width = max(len(str(element)) for row in elements for element in row)
            for index, row in enumerate(elements):
                break_ = '[' if index == 0 else ' ['
                out += break_ + ' '.join([str(element).rjust(max_width) for element in row]) + ']'
                if index < self.n_rows - 1:
                    out += '\n'
            out += ']'

        return out

    def __str__(self):
        return repr(self)

    def __len__(self):
        return len(self.elements)

    def __eq__(self, other):
        return self.elements == other.elements

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        if isinstance(other, Matrix):
            cond = self.n_rows == other.n_rows
            cond = cond and self.n_cols == other.n_cols

            if not cond:
                raise c_ex_.MatrixDimensionsMismatch()

            if self._multi_rows() and other._multi_rows():
                row = [[self_element + other_element
                        for self_element, other_element in zip(self_row, other_row)]
                       for self_row, other_row in zip(self.elements, other.elements)]
            else:
                row = [self_element + other_element
                       for self_element, other_element in zip(self.elements, other.elements)]

            return self._give_output(row)

        elif isinstance(other, (int, float)):
            if self._multi_rows():
                result_elements = [[element + other for element in row] for row in self.elements]
            else:
                result_elements = [element + other for element in self.elements]

            return self._give_output(result_elements)

        else:
            raise ValueError("Unsupported operand type for addition.")

    def __sub__(self, other):
        return self.__add__(other=-1 * other)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return self._scalar_vector_multiplication(other=other)

        elif isinstance(other, Matrix):
            if self.n_cols != other.n_rows:
                raise c_ex_.MatrixDimensionsMismatch(f'Inner CxR={self.n_cols}x{other.n_rows}, not allowed.')

            if self._multi_rows():
                if other.n_cols == 1:
                    return self._multi_row_v_col_matrix(other)
                else:
                    return self._multi_matrix(other=other)
            else:
                if other._multi_rows():
                    return self._row_v_multi_row(other)
                else:
                    return self._row_v_col(other)

    __radd__ = __add__

    __rsub__ = __sub__

    __rmul__ = __mul__

    def __truediv__(self, other):
        if isinstance(other, Matrix):
            raise c_ex_.DivisionByMatrix()

        if self._multi_rows():
            answer = [[element / other for element in row] for row in self.elements]
        else:
            answer = [element / other for element in self.elements]

        return self._give_output(answer)

    def __neg__(self):
        negated_elements = [[-element for element in row] for row in self.elements]
        return self._give_output(negated_elements)

    def __pow__(self, power, modulo=None):
        if modulo is None:
            return map_to_matrix(self, lambda _: _**power)
        else:
            return map_to_matrix(self, lambda _: _**power % modulo)

    def __initialize_slicing(self, slice_object):
        start, stop, step = slice_object.indices(len(self))

        if start is None:
            start = 0
        if stop is None:
            stop = self.n_rows
        if step is None:
            step = 1

        return start, stop, step

    def __getitem__(self, index):
        if isinstance(index, slice):
            start, stop, step = self.__initialize_slicing(index)
            output = [self.elements[i] for i in range(start, stop, step)]

        elif isinstance(index, tuple):
            output, output_ = [], []
            row_slice, col_slice = index

            if isinstance(row_slice, slice):
                start, stop, step = self.__initialize_slicing(row_slice)
                output_ = [self.elements[i] for i in range(start, stop, step)]

            if isinstance(col_slice, slice):
                start, stop, step = self.__initialize_slicing(col_slice)
                output = [out_[start:stop:step] for out_ in output_]
        else:
            if isinstance(index, (int, float)):
                if index > len(self.elements):
                    raise c_ex_.IndexOutOfBounds()

            return self._give_output(self.elements[index]) if self._multi_rows() else self.elements[index]

        return self._give_output(output)

    def __setitem__(self, index, value):
        if index >= len(self.elements):
            raise c_ex_.IndexOutOfBounds()

        if isinstance(index, (slice, tuple)):
            raise c_ex_.SlicingNotAllowed()

        self.elements[index] = value

    @property
    def n_rows(self) -> int:
        return len(self.elements) if self._multi_rows() else 1

    @property
    def n_cols(self) -> int:
        return len(self.elements[0]) if self._multi_rows() else len(self.elements)

    @property
    def dim(self):
        return f'RxC: {self.n_rows}x{self.n_cols}'

    @property
    def is_square(self):
        return self.n_rows == self.n_cols

    @property
    def is_singular(self):
        return determinant(self.elements) == 0

    @property
    def trace(self):
        return sum([self.elements[i][i] for i in range(self.n_rows)])

    @property
    def in_fractions(self):
        fr_ = [[InFractions(j) for j in i] for i in self.elements]

        return self._give_output(fr_)

    @staticmethod
    def _give_output(output):
        return Matrix(output)

    def _multi_rows(self):
        return isinstance(self.elements[0], list)

    def _scalar_vector_multiplication(self, other):
        if self._multi_rows():
            result_elements = [[element * other for element in row] for row in self.elements]
        else:
            result_elements = [element * other for element in self.elements]

        return self._give_output(result_elements)

    def _row_v_col(self, other):
        row_v_col = [sum([k * l[0] for k, l in zip(self.elements, other.elements)])]

        return self._give_output(row_v_col)

    def _multi_matrix(self, other):
        result = []
        for row in self.elements:
            r_temp = []
            for c_row in other.t.elements:
                r_temp.append(sum([r_elem * c_elem for r_elem, c_elem in zip(row, c_row)]))
            result.append(r_temp)

        return self._give_output(result)

    def _row_v_multi_row(self, other):
        if other.n_cols == 1:
            mul_ = sum([sum([s_elem * o_elem[0]]) for o_elem, s_elem in zip(other.elements, self.elements)])
        else:
            temp_ = []
            for c_rw, r_rw in zip(self.elements, other.elements):
                temp_.append([c_rw * i for i in r_rw])

            mul_ = [sum([i[j] for i in temp_]) for j in range(len(temp_))]

        return self._give_output(mul_) if isinstance(mul_, list) and len(mul_) > 1 else mul_

    def _multi_row_v_col_matrix(self, other):
        multi_row_v_col_matrix = [[sum([self.elements[row][col] * other.elements[col][0]
                                        for col in range(self.n_cols)])] for row in range(self.n_rows)]
        return self._give_output(multi_row_v_col_matrix)

    def _transpose(self):
        n_rows, n_cols, elements, give_output = self.n_rows, self.n_cols, self.elements, self._give_output

        if len(self) == 0:
            return give_output([])

        if self._multi_rows():
            answer = [[elements[row][col] for row in range(n_rows)] for col in range(n_cols)]

            if n_cols == 1:
                answer = answer[0]

            transposed_elements = answer
        else:
            if self.n_cols > 1:
                transposed_elements = [[element] for element in elements]
            else:
                transposed_elements = list(elements)

        return give_output(transposed_elements)

    def is_symmetric(self):
        return self == self.t

    def is_orthogonal(self):
        return self * self.t == identity_matrix(self.n_rows, self.n_cols)

    def is_positive_definite(self) -> bool:
        zero_ = null_matrix(self.n_rows, 1) + 1

        if not self.is_symmetric():
            return False

        return vector_mag(zero_.t * self * zero_) > 0

    def determinant(self):
        return determinant(self.elements)

    def inverse(self):
        inv_ = Inverse(self.elements).inverse()
        return self._give_output(inv_)

    def adjoint_matrix(self):
        return (self.inverse() * self.determinant()).in_fractions

    def diagonal(self):
        null_ = null_matrix(self.n_rows)
        for i in range(self.n_rows):
            null_[i] = self.elements[i][i]

        return null_

    def diagonal_of_matrix(self):
        n_rows, n_cols, elements = self.n_rows, self.n_cols, self.elements

        identity_ = identity_matrix(n_rows, n_cols)
        for i in range(n_rows):
            identity_[i][i] = elements[i][i]

        return identity_

    @property
    def t(self):
        return self.transpose

    @property
    def transpose(self):
        return self._transpose()

    def hadamard_product(self, other):
        elements, o_elements = self.elements, other.elements

        result = [[i * j for i, j in zip(self_rows, other_rows)] for self_rows, other_rows in
                  zip(elements, o_elements)]

        return self._give_output(result)

    def elementwise_product(self, other):
        return self.hadamard_product(other)

    def is_multiplicative_inverse_of(self, other):
        return self * other == identity_matrix(self.n_rows, self.n_cols)

    def is_orthogonal_to(self, other):
        if self.dim != other.dim:
            raise c_ex_.MatrixDimensionsMismatch()

        return self * other.t == identity_matrix(self.n_rows, self.n_cols)

    def dot(self, other):
        if not isinstance(other, Matrix):
            raise ValueError('The other must be a Matrix object')

        return sum([i * j for i, j in zip(self.elements, other.elements)])


def determinant(matrix: Matrix or LList) -> float:
    """
    Calculate determinant of a given matrix.

    Parameters
    ----------
    matrix:
        The matrix for which the determinant is to be calculated.

    Returns
    -------
        Determinant of matrix.
    """

    def calculate_determinant(mat: Matrix or LList) -> IFloat:
        """
        Calculates the determinant.

        Parameters
        ----------
        mat:
            Matrix or sub-matrix

        Returns
        -------
            Determinant of the matrix or sub-matrix given.
        """

        len_mat, det = len(mat), 0

        if len_mat == 1:
            return mat[0][0]

        for element in range(len_mat):
            sub_matrix = [row[:element] + row[element + 1:] for row in mat[1:]]
            cofactor = mat[0][element] * ((-1)**element)
            det += cofactor * calculate_determinant(sub_matrix)

        return det

    matrix = matrix.elements if isinstance(matrix, Matrix) else matrix

    n_rows, n_cols = len(matrix), len(matrix[0])

    if n_rows != n_cols:
        raise c_ex_.NotASquareMatrix("Matrix must be square for determinant calculation.")

    return calculate_determinant(matrix)


def identity_matrix(n_rows: int, n_cols: OptIFloat = None, value: IFloat = 1) -> Matrix:
    """
    Generates an identity matrix of given number of rows and columns.

    Parameters
    ----------
    n_rows:
        Number of rows for the null matrix.
    n_cols:
        Number of columns for the null matrix.
    value:
        The value to set on diagonals. Defaults to 1.

    Returns
    -------
        Identity matrix.
    """

    if n_cols is not None and n_cols != n_rows:
        raise c_ex_.NotASquareMatrix('The identity matrix can not be rectangular.')

    n_cols = n_rows if n_cols is None else n_cols

    identity_ = null_matrix(n_rows, n_cols)

    if n_rows == n_cols == 1:
        return Matrix([1])
    else:
        for i in range(n_rows):
            identity_[i][i] = value

        return identity_


def null_matrix(n_rows: int, n_cols: OptIFloat = None) -> Matrix:
    """
    Generate a null matrix of given number of rows and columns.

    Parameters
    ----------
    n_rows:
        Number of rows for the null matrix.
    n_cols:
        Number of columns for the null matrix.

    Returns
    -------
        Null matrix.

    """

    n_cols = n_rows if n_cols is None else n_cols

    mat_ = Matrix([[0] * n_cols for _ in range(n_rows)])

    return mat_ if n_rows > 1 else mat_[0]


def vector_mag(vector: Matrix, squared: bool = False) -> IFloat:
    """
    Gives the magnitude of the vector.

    Parameters
    ----------
    vector:
        The vector for which the magnitude is to be found. The vector is generally a mx1 matrix.
    squared:
        Whether the value required should be squared or not. Default is False.

    Returns
    -------
        Magnitude of the vector, squared magnitude if ``squared`` is True.
    """

    if not isinstance(vector, Matrix):
        vector = Matrix(vector)

    if vector.n_cols == 1:
        vector_ = list(chain.from_iterable(vector.elements))
    else:
        vector_ = vector.elements

    vec_norm_ = sum([i**2 for i in vector_])

    return vec_norm_ if squared else sqrt(vec_norm_)


def matrix_copy(matrix: Matrix, overwrite: bool = False) -> Matrix:
    """
    Copy or make a deep-copy of the given matrix.

    Parameters
    ----------
    matrix:
        The matrix to make the copy of.
    overwrite:
        Whether to overwrite the original matrix or not.

    Returns
    -------
    Matrix:
        The copied matrix instance.
    """

    temp_ = Matrix(matrix) if not isinstance(matrix, Matrix) else matrix
    return temp_ if overwrite else Matrix(deepcopy(temp_.elements[:]))


def map_to_matrix(matrix: Matrix, function, apply_to: str = 'full'):
    """
    Apply a given function element-wise to a matrix.

    Parameters
    ----------
    matrix:
        The matrix to be mapped.
    function:
        A function that takes a single float as input and returns a float.
    apply_to:
        Where to apply the function, either 'diagonal', 'off-diagonal' or 'full'. Default is full.

    Returns
    -------
    Matrix
        A new matrix where the function has been applied element-wise.
    """

    matrix_ = matrix_copy(matrix, True)

    for i in range(matrix_.n_rows):
        for j in range(matrix_.n_cols):
            if apply_to == 'diagonal':
                if i == j:
                    matrix_[i][j] = function(matrix[i][j])
            elif apply_to == 'off-diagonal':
                if i != j:
                    matrix_[i][j] = function(matrix[i][j])
            elif apply_to == 'full':
                matrix_[i][j] = function(matrix[i][j])

    return matrix_


class InFractions:
    def __init__(self, decimal_value: IFloat):
        self.fraction = Fraction(decimal_value).limit_denominator()

    def __repr__(self) -> str:
        return str(self.fraction)

    @property
    def numerator(self) -> IFloat:
        return self.fraction.numerator

    @property
    def denominator(self) -> IFloat:
        return self.fraction.denominator


class Inverse:

    def __init__(self, matrix_elements: LList):
        self.elements = matrix_elements

    @staticmethod
    def _pivot_row(matrix, col):
        """Find the row with the largest absolute value in the current column."""
        max_val = 0
        max_row = -1
        for i in range(col, len(matrix)):
            if abs(matrix[i][col]) > max_val:
                max_val = abs(matrix[i][col])
                max_row = i
        return max_row

    @staticmethod
    def _swap_rows(matrix, i, j):
        """Swap two rows in the matrix."""
        matrix[i], matrix[j] = matrix[j], matrix[i]

    @staticmethod
    def _scale_row(matrix, row, factor):
        """Multiply a row by a scalar factor."""
        matrix[row] = [x * factor for x in matrix[row]]

    @staticmethod
    def _add_scaled_row(matrix, source_row, target_row, factor):
        """Add a scaled row to another row."""
        scaled_row = [x * factor for x in matrix[source_row]]
        matrix[target_row] = [x + y for x, y in zip(matrix[target_row], scaled_row)]

    def inverse(self):
        n_rows = len(self.elements)
        n_cols = len(self.elements[0])

        if n_rows != n_cols:
            raise c_ex_.NotASquareMatrix("Matrix must be square for inverse calculation.")

        augmented_matrix = [row[:] + [int(i == j) for j in range(n_rows)] for i, row in enumerate(self.elements)]

        for col in range(n_rows):
            pivot_row = self._pivot_row(augmented_matrix, col)
            if pivot_row == -1:
                raise ValueError("Matrix is singular (no unique inverse).")

            self._swap_rows(augmented_matrix, col, pivot_row)

            pivot_value = augmented_matrix[col][col]
            self._scale_row(augmented_matrix, col, 1.0 / pivot_value)

            for row in range(n_rows):
                if row != col:
                    factor = -augmented_matrix[row][col]
                    self._add_scaled_row(augmented_matrix, col, row, factor)

        inverse_matrix = [row[n_rows:] for row in augmented_matrix]

        return inverse_matrix
