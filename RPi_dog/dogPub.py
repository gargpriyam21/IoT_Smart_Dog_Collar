import paho.mqtt.client as client
from mpu6050 import mpu6050
import numpy as np
import time
from constants import *
from helpers import *


def get_mag(sensor):
    vals = [sensor.get_accel_data().get('x'), sensor.get_accel_data().get('y'), sensor.get_accel_data().get('z')]
    mag = 0
    for i in range(0, 3):
        # mag = mag + ((vals[i]-offset[i])**2)
        mag = mag + ((vals[i]) ** 2)
    return np.sqrt(mag)


"""
Main loop logic:
-Determines dog status using the "diff" variable
-diff is the difference between the accelerometer at rest (rest_val) and "avg_mag"
-avg_mag is a moving average of the accelerometer values
-Once the dog's status changes to "DogMoving" it will remain in this state until he remains still for approximatley 3 seconds
    -rest_counter keeps track of how long the dog has been still
    -rest_counter is reset if the dog moves again

"""

def calculate_dog_status(diff, mqtt_dog_publisher, rest_counter, status):
    if diff > move_threshold and status == "DogStill":
        rest_counter[0] = 0
        status = "DogMoving"
        mqtt_dog_publisher.publish(topic_send, status)
        print("Dog is moving")
    elif (diff < idle_threshold) & (status == "DogMoving"):
        rest_counter[0] = rest_counter[0] + 1
        # print(rest_counter)
        if rest_counter[0] >= 300:
            status = "DogStill"
            mqtt_dog_publisher.publish(topic_send, status)
            print("Dog is idle")
    return status


def main():
    mag = [0, 0, 0]
    status = "DogStill"
    mqtt_dog_publisher = client.Client()
    mqtt_dog_publisher.connect(BROKER, port=PORT)
    mpu = mpu6050(0x68)
    rest_counter = [0]

    while True:
        avg_mag = find_moving_average(mag, get_mag(mpu))
        diff = np.abs(rest_val - avg_mag)

        status = calculate_dog_status(diff, mqtt_dog_publisher, rest_counter, status)

        time.sleep(IMU_SAMPLING_RATE)
    # print(diff)


if __name__ == '__main__':
    main()
