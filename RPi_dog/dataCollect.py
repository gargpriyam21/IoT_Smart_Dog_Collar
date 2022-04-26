
from mpu6050 import mpu6050
import numpy as np
import datetime
import time
from constants import *
from helpers import *

"""
1) Propt task
2) Start task when dog moves
3) Collect timestamp: accel + gyro + label
4) Save to txt file
"""
def get_mag(sensor):
    vals = [sensor.get_accel_data().get('x'), sensor.get_accel_data().get('y'), sensor.get_accel_data().get('z')]
    mag = 0
    for i in range(0, 3):
        # mag = mag + ((vals[i]-offset[i])**2)
        mag = mag + ((vals[i]) ** 2)
    return np.sqrt(mag)


def calculate_dog_status(diff, rest_counter, status):
    if diff > move_threshold and status == "DogStill":
        rest_counter[0] = 0
        status = "DogMoving"
        print("Dog is moving")
    elif (diff < idle_threshold) & (status == "DogMoving"):
        rest_counter[0] = rest_counter[0] + 1
        # print(rest_counter)
        if rest_counter[0] >= 200:
            status = "DogStill"
            print("Dog is idle")
    return status


def main():
    print("What should data be labeled as?")
    print("1: Sit")
    print("2: Lay down")
    print("3: Spin")
    print("4: Walk")
    label = input("type 1,2,3 or 4")
    fileName = input("Enter file name: ")

    f = open(fileName, 'w')
    f.write("Timestamp, Xaccel, Yaccel, Zaccel, Xgyro, Ygyro, Zgyro, label")
    taskRunning = True
    dataCollecting = False
    status = "DogStill"
    mag = [rest_val]*3
    sensor = mpu6050(0x68)
    rest_counter = [0]
    row = ""

    while taskRunning:
        mag_mpu = get_mag(sensor)
        avg_mag = find_moving_average(mag, mag_mpu)
        diff = np.abs(rest_val - avg_mag)

        status = calculate_dog_status(diff, rest_counter, status)
        if status == "DogMoving":
            dataCollecting = True
            row = str(datetime.datetime.now()) + "," + str(sensor.get_accel_data().get('x'))+","+str(sensor.get_accel_data().get('y'))+ ","+ str(sensor.get_accel_data().get('z'))+","
            row = row + str(sensor.get_gyro_data().get('x'))+","+str(sensor.get_gyro_data().get('y'))+ ","+ str(sensor.get_gyro_data().get('z'))+","+label+"\n"
            f.write(row)
        
        if (dataCollecting == True) & (status == "DogStill"):
            taskRunning = False
        time.sleep(IMU_SAMPLING_RATE)
    print("Task Complete.")


if __name__ == '__main__':
    main()
