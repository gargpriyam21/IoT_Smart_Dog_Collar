import paho.mqtt.client as client
from mpu6050 import mpu6050
import numpy as np
import time
from constants import *
import json
from Triangulation.triangulation import *

mpu = mpu6050(0x68)
status = "Idle"

def dogNearBy(dog_coordinates):
    nearby_distance = calculate_eucleadian_distance(dog_coordinates['x'], dog_coordinates['y'],
                                                   TRASH_CAN_X_COORDINATE, TRASH_CAN_Y_COORDINATE)
    
    if trashcan_nearby(nearby_distance, TRASH_CAN_THRESHOLD):
        return True
    else:
        return False

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

def on_message(client, userdata, message):
    dog_coordinates = json.loads(message.payload.decode("utf-8"))

    if dogNearBy(dog_coordinates) and status != "Bumped":
        client.publish(TRASH_CAN_TOPIC, "DogNearBy", qos=2)
        print("Dog is near the trash can")

def main():
    global status

    trashCanClient = client.Client()
    trashCanClient.connect(BROKER, port=PORT)

    trashCanClient.subscribe(topic_position, qos=2)

    mag = [0,0,0]
    status = "Idle"
    trashCanClient.publish(TRASH_CAN_TOPIC, "TrashCanSafe", qos=2)
    offset = calibrate(mpu)

    while True:
        mag[2] = mag[1]
        mag[1] = mag[0]
        mag[0] = get_mag(mpu,offset)
        avg_mag = np.mean(mag)

        if (avg_mag > threshold) and (status == "Idle"):
            status = "Bumped"
            trashCanClient.publish(TRASH_CAN_TOPIC, "DogPlayingWithTrashCan", qos=2)
            print("Trashcan Bumped")
            time.sleep(3)
        
        elif (avg_mag < threshold) and (status == "Bumped"):
            status = "Idle"
            trashCanClient.publish(TRASH_CAN_TOPIC, "TrashCanSafe", qos=2)
            print("Trashcan not moving")
            
        time.sleep(IMU_SAMPLING_RATE)

if __name__ == '__main__':
    main()