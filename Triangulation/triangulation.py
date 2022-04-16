import time
from sympy import symbols, Eq, solve

def calculate_distance(txPower, rssi):
    N = 2
    difference = txPower - rssi
    distance = 10 ** ((difference) / (10 * N))
    return distance

def get_coordinates(x1,x2,x3,y1,y2,y3,r1,r2,r3):
    x, y = symbols('x,y')
    
    xcoef1 = 2*x2 - 2*x1
    xcoef2 = 2*x3 - 2*x2
    
    ycoef1 = 2*y2 - 2*y1
    ycoef2 = 2*y3 - 2*y2

    c1 = x2**2 - x1**2 + y2**2 - y1**2 + r1**2 - r2**2
    c2 = x3**2 - x2**2 + y3**2 - y2**2 + r2**2 - r3**2

    eq1 = Eq(xcoef1*x + ycoef1*y, c1)
    eq2 = Eq(xcoef2*x + ycoef2*y, c2)

    print(eq1)
    print(eq2)

    x_sol = solve((eq1, eq2), (x, y))
    print(x_sol)

    return x_sol[x], x_sol[y]

# print(get_coordinates(100,160,70,100,120,150,50,36.06,60.83))

# print(calculate_distance(-69,-60))
# print(calculate_distance(-69,-69))
# print(calculate_distance(-69,-80))