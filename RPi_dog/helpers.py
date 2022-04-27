import numpy as np
from constants import *
import time

def find_moving_average(continous_arr, new_value):
    continous_arr[2] = continous_arr[1]
    continous_arr[1] = continous_arr[0]
    continous_arr[0] = new_value
    moving_average = np.mean(continous_arr)
    return moving_average

def calibrate(sensors):
    #get 5 samples from x,y and z coordinates
    x = np.zeros(5)
    y = np.zeros(5)
    z = np.zeros(5)
    
    for i in range(0,5):
        x[i] = sensors.get_accel_data().get('x')
        y[i] = sensors.get_accel_data().get('y')
        z[i] = sensors.get_accel_data().get('z')
        time.sleep(IMU_SAMPLING_RATE)

    x_offset = np.mean(x)
    y_offset = np.mean(y)
    z_offset = np.mean(z)

    return [x_offset,y_offset,z_offset]

def get_mag(sensor, offset):
    vals = [sensor.get_accel_data().get('x'), sensor.get_accel_data().get('y')]
    mag = 0
    
    for i in range(0,2):
        mag = mag + ((vals[i]-offset[i])**2)
    return np.sqrt(mag)
