"""Created on Oct 07 16:51:13 2023"""
from typing import List


class DETERMINANT:

    def __init__(self, n_rows: int, n_cols: int) -> None:
        self.n_rows = n_rows
        self.n_cols = n_cols

    def _get_cofactor(self, j, matrix, sub_matrix):
        cofactor = matrix[0][j] * self.determinant(sub_matrix)
        return cofactor

    def determinant(self, matrix: List[List]):
        if self.n_rows != self.n_cols:
            raise ValueError("Matrix must be square for determinant calculation.")

        n = len(matrix)

        if n == 1:
            return matrix[0][0]

        det = 0
        for j in range(n):
            sub_matrix = [row[:j] + row[j + 1:] for row in matrix[1:]]
            cofactor = matrix[0][j] * ((-1)**j)  # The cofactor is the element times (-1)^j
            det += cofactor * self.determinant(sub_matrix)

        return det
