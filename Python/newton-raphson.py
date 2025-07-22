import numpy as np

def f(x):
    return x**3 - 2

def g(x):
    return 3*x**2

def newtonraphson(x0, tolerance = 0.001):
    x1 = x0 - f(x0) / g(x0)
    print(x1)

    if (np.abs(f(x1)) < tolerance):
        print(f"Root found at {x1}")
        return
    else:
        newtonraphson(x1)

newtonraphson(10)