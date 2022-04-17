import time
from collections import deque
from triangulation import *
from beacontools import BeaconScanner, EddystoneTLMFrame, EddystoneFilter
import time
from mpu6050 import mpu6050
import numpy as np

# Defining Constants

## Namespace of the beacons to be scanned
BEACON1_NAMESPACE = "12345678912345678913"
BEACON2_NAMESPACE = "12345678912345678914"
BEACON3_NAMESPACE = "12345678912345678914"

## Beacon 1 coordinates
BEACON1_X_COORDINATE = 0
BEACON1_Y_COORDINATE = 0

## Beacon 2 coordinates
BEACON2_X_COORDINATE = 0
BEACON2_Y_COORDINATE = 0

## Beacon 3 coordinates
BEACON3_X_COORDINATE = 0
BEACON3_Y_COORDINATE = 0

# Initializing the Tx power for each beacon
BEACON1_TXPOWER = -65   
BEACON2_TXPOWER = -65
BEACON3_TXPOWER = -65

# Creating Queue for the beacons
BEACON1_Q = deque()
BEACON2_Q = deque()
BEACON3_Q = deque()

# Creating array to store pas values and generate the moving average of the RSSI values
PAST_BEACON1_RSSI = [0, 0, 0]
PAST_BEACON2_RSSI = [0, 0, 0]
PAST_BEACON3_RSSI = [0, 0, 0]

# Initializing the Trash Can's X and Y coordinates
TRASH_CAN_X_COORDINATE = 0
TRASH_CAN_Y_COORDINATE = 0

# Defining the Threshold for the trash can nearby
TRASH_CAN_THRESHOLD = 0.5

# Defining the timeout for each data reading
TIMEOUT = 1


def beacon1_callback(bt_addr, rssi, packet, additional_info):
    global BEACON1_TXPOWER, PAST_BEACON1_RSSI 

    BEACON1_TXPOWER = int(packet.tx_power)

    BEACON1_RSSI = rssi

    PAST_BEACON1_RSSI[2] = PAST_BEACON1_RSSI[1]
    PAST_BEACON1_RSSI[1] = PAST_BEACON1_RSSI[0]
    PAST_BEACON1_RSSI[0] = BEACON1_RSSI

    BEACON1_AVG_RSSI = (PAST_BEACON1_RSSI[0] + PAST_BEACON1_RSSI[1] + PAST_BEACON1_RSSI[2]) / 3

    r1 = calculate_distance(BEACON1_TXPOWER, BEACON1_AVG_RSSI)

    BEACON1_Q.append(r1)

def beacon2_callback(bt_addr, rssi, packet, additional_info):
    global BEACON2_TXPOWER, PAST_BEACON2_RSSI 

    BEACON2_TXPOWER = int(packet.tx_power)

    BEACON2_RSSI = rssi

    PAST_BEACON2_RSSI[2] = PAST_BEACON2_RSSI[1]
    PAST_BEACON2_RSSI[1] = PAST_BEACON2_RSSI[0]
    PAST_BEACON2_RSSI[0] = BEACON2_RSSI

    BEACON2_AVG_RSSI = (PAST_BEACON2_RSSI[0] + PAST_BEACON2_RSSI[1] + PAST_BEACON2_RSSI[2]) / 3

    r2 = calculate_distance(BEACON2_TXPOWER, BEACON2_AVG_RSSI)

    BEACON2_Q.append(r2)

def beacon3_callback(bt_addr, rssi, packet, additional_info):
    global BEACON3_TXPOWER, PAST_BEACON3_RSSI 

    BEACON3_TXPOWER = int(packet.tx_power)

    BEACON3_RSSI = rssi

    PAST_BEACON3_RSSI[2] = PAST_BEACON3_RSSI[1]
    PAST_BEACON3_RSSI[1] = PAST_BEACON3_RSSI[0]
    PAST_BEACON3_RSSI[0] = BEACON3_RSSI

    BEACON3_AVG_RSSI = (PAST_BEACON3_RSSI[0] + PAST_BEACON3_RSSI[1] + PAST_BEACON3_RSSI[2]) / 3

    r3 = calculate_distance(BEACON3_TXPOWER, BEACON3_AVG_RSSI)

    BEACON3_Q.append(r3)

# def callback(bt_addr, rssi, packet, additional_info):
#     print("<%s, %d> %s %s" % (bt_addr, rssi, packet, additional_info))

import paho.mqtt.client as client

BROKER = '192.168.86.21'
PORT = 4000
KEEP_ALIVE = 100

topic_send = "ncsu/iot/TrashCanInDanger"

topic_position = "ncsu/iot/DogCoordinates"

mqtt_dog_publisher = client.Client()
mqtt_dog_publisher.connect(BROKER, port=PORT)




mpu = mpu6050(0x68)
threshold = 10 #must be above threshold to move dog from "idle" to "moving" state
IMU_SAMPLING_RATE = 0.01 #seconds

#Calibrate sensors to account for acceleration due to gravity
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





if __name__ == '__main__':
    mag = [0,0,0]
    status = "Idle"
    #Publish status
    offset = calibrate(mpu)

    BEACON1_scanner = BeaconScanner(callback=beacon1_callback,
        filter=EddystoneFilter(namespaces=BEACON1_NAMESPACE)
    )

    BEACON2_scanner = BeaconScanner(callback=beacon2_callback,
        filter=EddystoneFilter(namespaces=BEACON2_NAMESPACE)
    )

    BEACON3_scanner = BeaconScanner(callback=beacon3_callback,
        filter=EddystoneFilter(namespaces=BEACON3_NAMESPACE)
    )

    while True:

        BEACON1_scanner.start()
        BEACON2_scanner.start()
        BEACON3_scanner.start()
        mag[2] = mag[1]
        mag[1] = mag[0]
        mag[0] = get_mag(mpu,offset)
        avg_mag = np.mean(mag)

        if len(BEACON1_Q) > 0 and len(BEACON2_Q) > 0 and len(BEACON3_Q) > 0:
            r1 = BEACON1_Q.popleft()
            r2 = BEACON2_Q.popleft()
            r3 = BEACON3_Q.popleft()

            current_coordinates  = get_coordinates(BEACON1_X_COORDINATE, BEACON2_X_COORDINATE, BEACON3_X_COORDINATE, BEACON1_Y_COORDINATE, BEACON2_Y_COORDINATE, BEACON3_Y_COORDINATE, r1, r2, r3)

            """
            if dog is still and not moving:
                publish the coordinates to the topic "DogCoordinates" via MQTT

                also print published coordinates to the topic "DogCoordinates"
            """
            mqtt_dog_publisher.publish(topic_position,current_coordinates)

            nearby_distace = calculate_eucleadian_distance(current_coordinates[0], current_coordinates[1], TRASH_CAN_X_COORDINATE, TRASH_CAN_Y_COORDINATE)

            if trashcan_nearby(nearby_distace, TRASH_CAN_THRESHOLD):
                mqtt_dog_publisher.publish(topic_send,"DogNearBy")
                print("Dog is near the trash can")
            else:
                mqtt_dog_publisher.publish(topic_send,"")

        """
        if trashcan is moving:
            publish "DogPlayingWithTrashCan" to the topic "TrashCanInDanger" via MQTT
        else:
            publish "DogNotNearTrashCan" to the topic "TrashCanInDanger" via MQTT  
        
        """
        if (avg_mag > threshold) & (status == "Idle"):
            status = "Bumped"
            #Publish status
            mqtt_dog_publisher.publish(topic_send,"DogPlayingWithTrashCan")
            print("Trashcan Bumped")
            time.sleep(3)
        elif (avg_mag < threshold) & (status == "Bumped"):
            status = "Idle"
            mqtt_dog_publisher.publish(topic_send,"DogNotNearTrashCan")

            #Publish status
            print("Trashcan not moving")
            
        time.sleep(IMU_SAMPLING_RATE)
        
        
