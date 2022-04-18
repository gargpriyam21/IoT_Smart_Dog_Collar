import paho.mqtt.client as client
from mpu6050 import mpu6050
import numpy as np
import time

mpu = mpu6050(0x68)
move_threshold = 3 #must be above threshold to move dog from "idle" to "moving" state
idle_threshold = 2 #must be below threshold to move dog from "moving" to "idle" state
IMU_SAMPLING_RATE = 0.01 #seconds
BROKER = '192.168.1.163'
PORT = 4000
KEEP_ALIVE = 100

topic_send = "ncsu/iot/DogWalkingStatus"

mqtt_dog_publisher = client.Client()
mqtt_dog_publisher.connect(BROKER, port=PORT)


def get_mag(sensor):
    vals = [sensor.get_accel_data().get('x'), sensor.get_accel_data().get('y'), sensor.get_accel_data().get('z')]
    mag = 0
    for i in range(0,3):
        #mag = mag + ((vals[i]-offset[i])**2)
        mag = mag + ((vals[i])**2)
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

def main():
    mag = [0,0,0]
    status = "DogStill"
    while True:
        mag[2] = mag[1]
        mag[1] = mag[0]
        mag[0] = get_mag(mpu)
        avg_mag = np.mean(mag)
        diff = np.abs(rest_val - avg_mag)
        if (diff > move_threshold):
            rest_counter = 0
            if (status == "DogStill"):
                status = "DogMoving"
				mqtt_dog_publisher.publish(topic_send,status)
                print("Dog is moving")
        elif (diff < idle_threshold) & (status == "DogMoving"):
            rest_counter = rest_counter+1
            #print(rest_counter)
            if rest_counter >= 300:
                status = "DogStill"
				mqtt_dog_publisher.publish(topic_send,status)
                print("Dog is idle")

        time.sleep(IMU_SAMPLING_RATE)
        #print(diff)

if __name__ == '__main__':
    main()




