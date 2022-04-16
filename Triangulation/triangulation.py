import time
from sympy import symbols, Eq, solve

def calculate_distance(txPower, rssi):
    N = 2
    difference = txPower - rssi
    distance = 10 ** ((difference) / (10 * N))
    return distance


# print(calculate_distance(-69,-60))
# print(calculate_distance(-69,-69))
# print(calculate_distance(-69,-80))