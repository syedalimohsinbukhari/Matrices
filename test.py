"""Created on Oct 05 00:47:23 2023"""

from icecream import ic

from Matrix import Matrix

t1 = Matrix([[3, 0], [-1, 2]])
t2 = Matrix([[6], [5]])

ic(t1 * t2)
