# 
import numpy as np


def find_moving_average(continous_arr, new_value):
    continous_arr[2] = continous_arr[1]
    continous_arr[1] = continous_arr[0]
    continous_arr[0] = new_value
    moving_average = np.mean(continous_arr)
    return moving_average