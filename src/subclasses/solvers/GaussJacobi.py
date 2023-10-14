"""Created on Oct 13 11:37:27 2023"""

from fractions import Fraction

import matplotlib.pyplot as plt
from icecream import ic

from Matrix import Matrix


class GaussJacobi:

    def __init__(self, system_of_equations: Matrix, solution: Matrix, n_iter: int = 10, tol: float = 1e-5,
                 initial_guess: tuple = (0, 0, 0)):
        self.tol = tol
        self.n_iter = n_iter
        self.solution = solution
        self.initial_guess = initial_guess
        self.system_of_equations = system_of_equations.elements

        self.arr1, self.arr2, self.arr3 = [], [], []

    def _string(self):
        f1 = f'({Fraction(1, self.system_of_equations[0][0])})*'
        f1 += f'({self.solution[0][0]}'
        f1 += f' - ({self.system_of_equations[0][1]}*{self.initial_guess[1]})'
        f1 += f' - ({self.system_of_equations[0][2]}*{self.initial_guess[2]}))'

        ic(f1, eval(f1))

        f2 = f'({Fraction(1, self.system_of_equations[1][1])})*'
        f2 += f'({self.solution[1][0]}'
        f2 += f' - ({self.system_of_equations[1][0]}*{self.initial_guess[0]})'
        f2 += f' - ({self.system_of_equations[1][2]}*{self.initial_guess[2]}))'

        ic(f2, eval(f2))

        f3 = f'({Fraction(1, self.system_of_equations[2][2])})*'
        f3 += f'({self.solution[2][0]}'
        f3 += f' - ({self.system_of_equations[2][0]}*{self.initial_guess[0]})'
        f3 += f' - ({self.system_of_equations[2][1]}*{self.initial_guess[1]}))'

        ic(f3, eval(f3))

    def _evaluate(self):
        p1 = self.solution[0]
        p1 -= self.system_of_equations[0][1] * self.initial_guess[1]
        p1 -= self.system_of_equations[0][2] * self.initial_guess[2]
        p1 = p1[0] * self.system_of_equations[0][0]**-1

        p2 = self.solution[1]
        p2 -= self.system_of_equations[1][0] * self.initial_guess[0]
        p2 -= self.system_of_equations[1][2] * self.initial_guess[2]

        p2 = p2[0] * self.system_of_equations[1][1]**-1

        p3 = self.solution[2]
        p3 -= self.system_of_equations[2][0] * self.initial_guess[0]
        p3 -= self.system_of_equations[2][1] * self.initial_guess[1]

        p3 = p3[0] * self.system_of_equations[2][2]**-1

        self.arr1.append(p1)
        self.arr2.append(p2)
        self.arr3.append(p3)

        return [p1, p2, p3]

    def solve(self, in_string=False):
        for iter_ in range(self.n_iter):
            self.initial_guess = self._evaluate()
            if in_string:
                self._string()

        return Matrix(self.initial_guess).transpose()

    def plot_solutions(self, iterations, den_limit=20):
        x = range(len(self.arr1))
        plt.plot(x, self.arr1, 'ko--', label=r'$X_1$ = ' + f'{Fraction(self.arr1[-1]).limit_denominator(den_limit)}')
        plt.plot(x, self.arr2, 'go--', label=r'$X_2$ = ' + f'{Fraction(self.arr2[-1]).limit_denominator(den_limit)}')
        plt.plot(x, self.arr3, 'bo--', label=r'$X_3$ = ' + f'{Fraction(self.arr3[-1]).limit_denominator(den_limit)}')
        plt.title(f'Solution parameters using {iterations} iterations')
        plt.legend(loc='best')
        plt.tight_layout()

        plt.show()
