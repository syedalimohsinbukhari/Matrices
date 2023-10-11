from fractions import Fraction as PyFraction


class FRACTION:
    def __init__(self, decimal):
        self.fraction = PyFraction(decimal).limit_denominator()

    def __str__(self):
        return str(self.fraction)

    @property
    def numerator(self):
        return self.fraction.numerator

    @property
    def denominator(self):
        return self.fraction.denominator
