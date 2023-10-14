"""Created on Oct 08 18:22:21 2023"""

from fractions import Fraction


class FRACTION:
    def __init__(self, decimal):
        self.fraction = Fraction(decimal).limit_denominator()

    def __str__(self):
        return str(self.fraction)

    @property
    def numerator(self):
        return self.fraction.numerator

    @property
    def denominator(self):
        return self.fraction.denominator
