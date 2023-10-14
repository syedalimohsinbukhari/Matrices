"""Created on Oct 07 17:48:12 2023"""

import subclasses.EXCEPTIONS_ as EX_
from subclasses.DETERMINANT_ import DETERMINANT
from subclasses.FRACTION_ import FRACTION
from subclasses.INVERSE_ import INVERSE
from subclasses.specials.IDENTITY_ import IDENTITY


class MATRIX:

    def __init__(self, elements):
        self.elements = elements

    def __repr__(self):
        out = ''
        if self.n_rows == 1:
            max_width = max(len(str(row)) for row in self.elements)
            out += '[' + ' '.join([str(element).rjust(max_width) for element in self.elements]) + ']'
        else:
            out = '['
            max_width = max(len(str(element)) for row in self.elements for element in row)
            for index, row in enumerate(self.elements):
                br = '[' if index == 0 else ' ['
                out += br + ' '.join([str(element).rjust(max_width) for element in row]) + ']'
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
        if isinstance(other, MATRIX):
            cond = self.n_rows == other.n_rows
            cond = cond and self.n_cols == other.n_cols

            if not cond:
                raise EX_.MatrixDimensionsMismatch()

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

        elif isinstance(other, MATRIX):
            if self.n_cols != other.n_rows:
                raise EX_.MatrixDimensionsMismatch(f'Inner CxR={self.n_cols}x{other.n_rows}, not allowed.')

            if self._multi_rows():
                return self._multi_matrix(other=other)
            else:
                return self._row_v_multi_row(other=other) if other._multi_rows() else self._row_v_col(other=other)

    __radd__ = __add__

    __rsub__ = __sub__

    __rmul__ = __mul__

    def __truediv__(self, other):
        if isinstance(other, MATRIX):
            raise EX_.DivisionByMatrix()

        if self._multi_rows():
            answer = [[element / other for element in row] for row in self.elements]
        else:
            answer = [element / other for element in self.elements]

        return self._give_output(answer)

    def __neg__(self):
        negated_elements = [[-element for element in row] for row in self.elements]
        return self._give_output(negated_elements)

    def __getitem__(self, index):
        if isinstance(index, int) and index >= len(self.elements):
            raise EX_.IndexOutOfBounds()

        if isinstance(index, slice):
            raise EX_.SlicingNotAllowed()

        return self._give_output(self.elements[index]) if self._multi_rows() else self.elements[index]

    def __setitem__(self, index, value):
        if isinstance(index, int) and index >= len(self.elements):
            raise EX_.IndexOutOfBounds()

        if isinstance(index, slice):
            raise EX_.SlicingNotAllowed()

        self.elements[index] = value

    @property
    def n_rows(self):
        return len(self.elements) if self._multi_rows() else 1

    @property
    def n_cols(self):
        return len(self.elements[0]) if self._multi_rows() else len(self.elements)

    @property
    def dim(self):
        return f'RxC: {self.n_rows}x{self.n_cols}'

    @property
    def is_singular(self):
        return True if DETERMINANT(self.n_rows, self.n_cols).determinant(self.elements) == 0 else False

    @property
    def trace(self):
        return sum([self.elements[i][i] for i in range(self.n_rows)])

    @property
    def in_fractions(self):
        fr_ = [[FRACTION(j).fraction for j in i] for i in self.elements]

        return self._give_output(fr_)

    @property
    def adjoint_matrix(self):
        inv_ = self._give_output(INVERSE(self.elements).inverse())
        det_ = DETERMINANT(self.n_rows, self.n_cols).determinant(self.elements)

        return (inv_ * det_).in_fractions

    @property
    def diagonal(self):
        n_m = IDENTITY(self.n_rows).matrix()
        for i in range(self.n_rows):
            n_m[i][i] = self.elements[i][i]

        return self._give_output(n_m)

    @staticmethod
    def _give_output(output):
        return MATRIX(output)

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
        row1 = []
        for i in self.elements:
            row2 = []
            for j in other._transpose().elements:
                row2.append(sum([k * l for k, l in zip(i, j)]))
            row1.append(row2)

        return self._give_output(row1)

    def _row_v_multi_row(self, other):
        row_v_multi_row = [[sum([i * l for i, l in zip(self.elements, j)])] for j in other._transpose().elements]

        return self._give_output(row_v_multi_row)

    def _transpose(self):
        if len(self) == 0:
            return self._give_output([])

        if self._multi_rows():
            answer = [[self.elements[j][i] for j in range(len(self))] for i in range(len(self[0]))]
            if self.n_cols == 1:
                answer = answer[0]

            transposed_elements = answer
        else:
            transposed_elements = [element for element in self.elements]

        return self._give_output(transposed_elements)

    def transpose(self):
        return self._transpose()

    def inverse(self, separate_determinant=False):
        return self._give_output(INVERSE(self.elements).inverse())

    def determinant(self):
        return DETERMINANT(self.n_rows, self.n_cols).determinant(self.elements)
