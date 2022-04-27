import paho.mqtt.client as client
from mpu6050 import mpu6050
import numpy as np
import time

mpu = mpu6050(0x68)
move_threshold = 2 #must be above threshold to move dog from "idle" to "moving" state
idle_threshold = 0.5 #must be below threshold to move dog from "moving" to "idle" state
rest_val = 9.8 #net acceleration when dog is idle (acceleration due to gravity)
IMU_SAMPLING_RATE = 0.01 #seconds




def get_mag(sensor):
    vals = [sensor.get_accel_data().get('x'), sensor.get_accel_data().get('y'), sensor.get_accel_data().get('z')]
    mag = 0
    for i in range(0,3):
        mag = mag + ((vals[i])**2)
    return np.sqrt(mag)

def main():
    mag = [0,0,0]
    rest_counter = 0
    status = "DogStill"

    while True:
        mag[2] = mag[1]
        mag[1] = mag[0]
        mag[0] = get_mag(mpu)
        avg_mag = np.mean(mag)
        diff = np.abs(rest_val - avg_mag)

        if (diff > 3):
            rest_counter = 0
            if (status == "DogStill"):
                status = "DogMoving"
                print("Dog is moving")
        elif (diff < 2) & (status == "DogMoving"):
            rest_counter = rest_counter+1
            #print(rest_counter)
            if rest_counter >= 300:
                status = "DogStill"
                print("Dog is idle")
        #publish status to dog topic
        time.sleep(IMU_SAMPLING_RATE)
        #print(diff)
if __name__ == '__main__':
    main()




