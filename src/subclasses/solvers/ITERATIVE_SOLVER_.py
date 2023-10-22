"""Created on Oct 14 06:07:34 2023"""

from fractions import Fraction

from icecream import ic

from Matrix import Matrix


# TODO: return the arr1, arr2, arr3 for plotting with sensible names

class IterativeSolver:
    def __init__(self, system_of_equations: Matrix, solution: Matrix, n_iter: int = 10, tol: float = 1e-5,
                 initial_guess: tuple = (0, 0, 0)):
        self.tol = tol
        self.n_iter = n_iter
        self.solution = solution
        self.initial_guess = initial_guess
        self.system_of_equations = system_of_equations.elements
        self.arr1, self.arr2, self.arr3 = [], [], []

    def _evaluate(self):
        iter1_ = self.solution[0]
        iter1_ -= self.system_of_equations[0][1] * self.initial_guess[1]
        iter1_ -= self.system_of_equations[0][2] * self.initial_guess[2]
        iter1_ = iter1_[0] * self.system_of_equations[0][0]**-1

        iter2_ = self.solution[1]

        if self.__class__.__name__ == 'GaussJacobi':
            iter2_ -= self.system_of_equations[1][0] * self.initial_guess[0]
        else:
            iter2_ -= self.system_of_equations[1][0] * iter1_

        iter2_ -= self.system_of_equations[1][2] * self.initial_guess[2]
        iter2_ = iter2_[0] * self.system_of_equations[1][1]**-1

        iter3_ = self.solution[2]

        if self.__class__.__name__ == 'GaussJacobi':
            iter3_ -= self.system_of_equations[2][0] * self.initial_guess[0]
            iter3_ -= self.system_of_equations[2][1] * self.initial_guess[1]
        else:
            iter3_ -= self.system_of_equations[2][0] * iter1_
            iter3_ -= self.system_of_equations[2][1] * iter2_

        iter3_ = iter3_[0] * self.system_of_equations[2][2]**-1

        self.arr1.append(iter1_)
        self.arr2.append(iter2_)
        self.arr3.append(iter3_)

        return [iter1_, iter2_, iter3_]

    def _string(self):
        str1_ = f'({self.solution[0][0]}'
        str1_ += f' - ({self.system_of_equations[0][1]}*{self.initial_guess[1]})'
        str1_ += f' - ({self.system_of_equations[0][2]}*{self.initial_guess[2]}))'

        str1_ = f'({Fraction(1, self.system_of_equations[0][0])})*{str1_}'

        ic(str1_, eval(str1_))

        str2_ = f'({self.solution[1][0]}'

        if self.__class__.__name__ == 'GaussJacobi':
            str2_ += f' - ({self.system_of_equations[1][0]}*{self.initial_guess[0]})'
        else:
            str2_ += f' - ({self.system_of_equations[1][0]}*{eval(str1_)})'

        str2_ += f' - ({self.system_of_equations[1][2]}*{self.initial_guess[2]}))'

        str2_ = f'({Fraction(1, self.system_of_equations[1][1])})*{str2_}'

        ic(str2_, eval(str2_))

        str3_ = f'({self.solution[2][0]}'

        if self.__class__.__name__ == 'GaussJacobi':
            str3_ += f' - ({self.system_of_equations[2][0]}*{self.initial_guess[0]})'
            str3_ += f' - ({self.system_of_equations[2][1]}*{self.initial_guess[1]}))'
        else:
            str3_ += f' - ({self.system_of_equations[2][0]}*{eval(str1_)})'
            str3_ += f' - ({self.system_of_equations[2][1]}*{eval(str2_)}))'

        str3_ = f'({Fraction(1, self.system_of_equations[2][2])})*{str3_}'

        ic(str3_, eval(str3_))

    def solve(self, in_string=False):
        for iter_ in range(self.n_iter):
            if in_string:
                self._string()
            self.initial_guess = self._evaluate()
        return Matrix(self.initial_guess).transpose()
