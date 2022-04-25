import time
from collections import deque
from triangulation import *
from beacontools import BeaconScanner, EddystoneTLMFrame, EddystoneFilter
import time
from mpu6050 import mpu6050
import numpy as np
from constants import *
import paho.mqtt.client as client
from copy import deepcopy
import json

# Creating Queue for the beacons
BEACON1_Q = deque()
BEACON2_Q = deque()
BEACON3_Q = deque()

# Creating array to store pas values and generate the moving average of the RSSI values
PAST_BEACON1_RSSI = [0, 0, 0]
PAST_BEACON2_RSSI = [0, 0, 0]
PAST_BEACON3_RSSI = [0, 0, 0]

current_dog_coordinates = {"x": 0, "y": 0}
dog_moving_status_subscriber = client.Client("Triangulation")
publish_dog_coordinates = False

def calculate_dog_position():
    """
    Calculates the dog's position based on the RSSI values of the beacons
    """

    global  current_dog_coordinates, BEACON1_Q, BEACON2_Q, BEACON3_Q, publish_dog_coordinates, dog_moving_status_subscriber

    if len(BEACON1_Q) > 0 and len(BEACON2_Q) > 0 and len(BEACON3_Q) > 0:
        if not BEACON1_Q:
            return
        if not BEACON2_Q:
            return
        if not BEACON3_Q:
            return
        
        r1 = BEACON1_Q.popleft()
        r2 = BEACON2_Q.popleft()
        r3 = BEACON3_Q.popleft()

        current_dog_coordinates = get_coordinates(BEACON1_X_COORDINATE, BEACON2_X_COORDINATE, BEACON3_X_COORDINATE,
                                              BEACON1_Y_COORDINATE, BEACON2_Y_COORDINATE, BEACON3_Y_COORDINATE, r1,
                                              r2, r3)
        # print(len(BEACON1_Q), " ", len(BEACON2_Q), " ", len(BEACON3_Q), " ", current_dog_coordinates)

        if publish_dog_coordinates:
            dog_moving_status_subscriber.publish(topic_position, str(current_dog_coordinates).replace("'",'"'))


def get_radius(TxPower, RSSI_values):
    distances = []

    def weighted_average(arr):
        weights = [2] + [1]*(len(arr)-1)
        return np.average(np.array(arr), weights=np.array(weights))

    d3 = calculate_distance(TxPower, RSSI_values[2])
    d2 = calculate_distance(TxPower, RSSI_values[1])
    d1 = calculate_distance(TxPower, RSSI_values[0])

    if RSSI_values[0] != 0:
        distances.append(d1)

    if RSSI_values[1] != 0:
        distances.append(d2)

    if RSSI_values[2] != 0:
        distances.append(d3)

    if len(distances) != 0:
        radius = weighted_average(distances)
    else:
        radius = 0
    
    return radius
    

def beacon1_callback(bt_addr, rssi, packet, additional_info):
    global BEACON1_TXPOWER, PAST_BEACON1_RSSI

    BEACON1_TXPOWER = int(packet.tx_power)

    BEACON1_RSSI = rssi

    PAST_BEACON1_RSSI[2] = PAST_BEACON1_RSSI[1]
    PAST_BEACON1_RSSI[1] = PAST_BEACON1_RSSI[0]
    PAST_BEACON1_RSSI[0] = BEACON1_RSSI

    r1 = get_radius(BEACON1_TXPOWER, deepcopy(PAST_BEACON1_RSSI))

    BEACON1_Q.append(r1)

    # calculate_dog_position()


def beacon2_callback(bt_addr, rssi, packet, additional_info):
    global BEACON2_TXPOWER, PAST_BEACON2_RSSI

    BEACON2_TXPOWER = int(packet.tx_power)

    BEACON2_RSSI = rssi

    PAST_BEACON2_RSSI[2] = PAST_BEACON2_RSSI[1]
    PAST_BEACON2_RSSI[1] = PAST_BEACON2_RSSI[0]
    PAST_BEACON2_RSSI[0] = BEACON2_RSSI

    r2 = get_radius(BEACON2_TXPOWER, deepcopy(PAST_BEACON2_RSSI))

    BEACON2_Q.append(r2)

    # calculate_dog_position()


def beacon3_callback(bt_addr, rssi, packet, additional_info):
    global BEACON3_TXPOWER, PAST_BEACON3_RSSI

    BEACON3_TXPOWER = int(packet.tx_power)

    BEACON3_RSSI = rssi

    PAST_BEACON3_RSSI[2] = PAST_BEACON3_RSSI[1]
    PAST_BEACON3_RSSI[1] = PAST_BEACON3_RSSI[0]
    PAST_BEACON3_RSSI[0] = BEACON3_RSSI

    r3 = get_radius(BEACON3_TXPOWER, deepcopy(PAST_BEACON3_RSSI))

    BEACON3_Q.append(r3)

    # calculate_dog_position()

def on_callback(bt_addr, rssi, packet, additional_info):

    if packet.namespace == BEACON1_NAMESPACE:
        # print("beacon 1 rssi = ", rssi)cl
        beacon1_callback(bt_addr, rssi, packet, additional_info)
    elif packet.namespace == BEACON2_NAMESPACE:
        # print("beacon 2 rssi = ", rssi)
        beacon2_callback(bt_addr, rssi, packet, additional_info)
    elif packet.namespace == BEACON3_NAMESPACE:
        # print("beacon 3 rssi = ", rssi)
        beacon3_callback(bt_addr, rssi, packet, additional_info)

    calculate_dog_position()

def on_connect(client, userdata, flags, rc):
    print("Connected to the Broker with result code "+str(rc))

def on_message(client, userdata, message):
    global publish_dog_coordinates, current_dog_coordinates
    dog_moving_status = str(message.payload.decode("utf-8"))
    if dog_moving_status == "DogMoving":
        client.publish(topic_position, str(current_dog_coordinates).replace("'",'"'))
        publish_dog_coordinates = True
    elif dog_moving_status == "DogStill":
        publish_dog_coordinates = False


def main():
    beacon_scanner = BeaconScanner(callback=on_callback,
                                    device_filter=[EddystoneFilter(namespace=BEACON1_NAMESPACE),EddystoneFilter(namespace=BEACON2_NAMESPACE),EddystoneFilter(namespace=BEACON3_NAMESPACE)]
                                    )

    dog_moving_status_subscriber.on_connect = on_connect
    dog_moving_status_subscriber.on_message = on_message
    dog_moving_status_subscriber.connect(BROKER, port=PORT, keepalive=KEEP_ALIVE)
    dog_moving_status_subscriber.loop_start()
    dog_moving_status_subscriber.subscribe(topic_subscribe)
    
    beacon_scanner.start()

    while True:
        time.sleep(TIMEOUT)
        BEACON1_Q.clear()
        BEACON2_Q.clear()
        BEACON3_Q.clear()


if __name__ == '__main__':
    main()
