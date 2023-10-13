"""Created on Oct 13 06:59:35 2023"""


class IDENTITY:

    def __init__(self, n_rows):
        self.n_rows = n_rows

    def matrix(self):
        identity_matrix = [[0 for _ in range(self.n_rows)] for _ in range(self.n_rows)]

        for i in range(self.n_rows):
            identity_matrix[i][i] = 1

        return identity_matrix
