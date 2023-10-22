"""Created on Oct 19 03:46:05 2023"""
import copy

from icecream import ic


class InterpolationException(Exception):
    pass


class AtLeastOneParameterRequired(InterpolationException):
    pass


# TODO: correct implementation of INTERPOLATION method


class INTERPOLATION:

    def __init__(self, given_values, value_to_approximate, function=None, function_values=None):
        self.given_values = given_values
        self.value_to_approx = value_to_approximate

        if function is None and function_values is None:
            raise AtLeastOneParameterRequired("One of `function` or `function_values` parameter is required.")

        self.function = function if function else None
        self.function_values = function_values if function_values else None

    def _class(self):
        return 'Fwd' if self.__class__.__name__ == 'FwdInterpolation' else 'Bkw'

    def difference_table(self, table_limit=None):
        idx_ = self._get_x0()
        table_limit = len(self.given_values) - 1 if not table_limit else table_limit

        difference_table = [self.function_values]

        for i in range(table_limit):
            temp_ = []
            for j, k in zip(difference_table[-1][:-1], difference_table[-1][1:]):
                temp_.append(round(k - j, 4))

            difference_table.append(temp_)

        if self._class() == 'Fwd':
            return difference_table[:-idx_] if idx_ > 0 else difference_table
        elif self._class() == 'Bkw':
            return difference_table[0:idx_ + 1]

    def solve(self):
        def factorial(number):
            return 1 if number == 0 else number * factorial(number - 1)

        idx_ = self._get_x0()
        difference_table = self.difference_table()[1:] if self._class() == 'Fwd' else self.difference_table()[1:]
        initial_value = self.function_values[idx_]

        result = [initial_value]
        iter_condition = len(self.given_values) - 1
        iter_condition = iter_condition - idx_ if self._class() == 'Fwd' else iter_condition

        _, p_value = self._p(), [self._p()]
        for i in range(1, iter_condition):
            _ *= self._p() - i if self._class() == 'Fwd' else self._p() + i
            p_value.append(_)

        for i in range(iter_condition):
            if self._class() == 'Fwd':
                value = difference_table[-1][0] if i == iter_condition - 1 else difference_table[i][idx_]
            else:
                temp_ = difference_table[i]
                value = difference_table[-1][0] if i == iter_condition - 1 else temp_[len(temp_) - 1]

            result.append((value * p_value[i]) / factorial(i + 1))

        return result, sum(result)

    def _p(self):
        if self._class() == 'Fwd':
            num_ = self.value_to_approx - self.given_values[0]
        else:
            num_ = self.value_to_approx - self.given_values[-1]

        return num_ / (self.given_values[1] - self.given_values[0])

    def _get_x0(self):
        temp_ = copy.deepcopy(self.given_values)
        temp_.insert(0, self.value_to_approx)
        temp_.sort()

        return temp_.index(self.value_to_approx) - 1 if self._class() == 'Fwd' else len(self.given_values) - 1


class FwdInterpolation(INTERPOLATION):
    pass


class BkwInterpolation(INTERPOLATION):
    pass


c = BkwInterpolation([1891, 1901, 1911, 1921, 1931], 1929, function_values=[46, 66, 81, 93, 101])
ic(c.difference_table())
ic(c.solve())
