"""Created on Oct 07 16:47:20 2023"""

from typing import List


class INVERSE:

    def __init__(self, matrix_elements: List[List]):
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
        n = len(self.elements)
        if n != len(self.elements[0]):
            raise ValueError("Matrix must be square for inverse calculation.")

        # Create an augmented matrix [A | I]
        augmented_matrix = [row[:] + [int(i == j) for j in range(n)] for i, row in enumerate(self.elements)]

        for col in range(n):
            pivot_row = self._pivot_row(augmented_matrix, col)
            if pivot_row == -1:
                raise ValueError("Matrix is singular (no unique inverse).")

            self._swap_rows(augmented_matrix, col, pivot_row)

            pivot_value = augmented_matrix[col][col]
            self._scale_row(augmented_matrix, col, 1.0 / pivot_value)

            for row in range(n):
                if row != col:
                    factor = -augmented_matrix[row][col]
                    self._add_scaled_row(augmented_matrix, col, row, factor)

        # Extract the inverse part of the augmented matrix
        inverse_matrix = [row[n:] for row in augmented_matrix]

        return inverse_matrix
