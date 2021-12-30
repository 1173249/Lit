from sympy import *
import numpy as np
x = Symbol('x')

y = Symbol('y')

print(solve([2.9125255623e-05 * x * x + 915.990068056 * x -325177.155446 - y, (x - 356) ** 2 + (y - 919) **2 - np.square(405.77087130546965) ],[x,y]))

print(solve([y**4 - 1], [y]))
