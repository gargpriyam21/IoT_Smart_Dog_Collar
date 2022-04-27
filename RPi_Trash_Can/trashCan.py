import paho.mqtt.client as client
from mpu6050 import mpu6050
import numpy as np
import time
from constants import *
import json

mpu = mpu6050(0x68)
status = "Idle"

# def dogNearBy(dog_nearby_status):
#     if dog_nearby_status == "DogNearby":
#         return True
#     else:
#         return False

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

dog_nearby = False
def on_message(client, userdata, message):
    global dog_nearby
    dog_nearby_status = message.payload.decode("utf-8")
    print(dog_nearby_status)

    if dog_nearby_status == "DogNearby":
        dog_nearby = True
    else:
        dog_nearby = False
        
def on_connect(client, userdata, flags, rc):
    print("Connected to the Broker with result code "+str(rc))


def main():
    global status, dog_nearby

    trashCanClient = client.Client("TrashCan")
    trashCanClient.on_message = on_message
    trashCanClient.on_connect = on_connect
    trashCanClient.connect(BROKER, port=PORT)
    count_idle = 0

    trashCanClient.loop_start()
    trashCanClient.subscribe(topic_inform_trashcan, qos=2)

    mag = [0,0,0]
    status = "Idle"
    trashCanClient.publish(TRASH_CAN_TOPIC, "TrashCanSafe", qos=2)
    offset = calibrate(mpu)

    while True:
        mag[2] = mag[1]
        mag[1] = mag[0]
        mag[0] = get_mag(mpu,offset)
        avg_mag = np.mean(mag)
        # print(avg_mag)

        if (avg_mag > threshold) and (status == "Idle") and dog_nearby:
            status = "Bumped"
            trashCanClient.publish(TRASH_CAN_TOPIC, "DogPlayingWithTrashCan", qos=2)
            print("Trashcan Bumped")
            time.sleep(3)
        
        elif (avg_mag < 1.5) and (status == "Bumped"):
            count_idle += 1
            time.sleep(0.25)
            if count_idle == 3:
                status = "Idle"
                trashCanClient.publish(TRASH_CAN_TOPIC, "TrashCanSafe", qos=2)
                print("Trashcan not moving")
                count_idle = 0
        time.sleep(IMU_SAMPLING_RATE)

if __name__ == '__main__':
    main()