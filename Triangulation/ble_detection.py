import time
from collections import deque
from triangulation import *
from beacontools import BeaconScanner, EddystoneTLMFrame, EddystoneFilter
import time
from mpu6050 import mpu6050
import numpy as np
from constants import *
import paho.mqtt.client as client

# Creating Queue for the beacons
BEACON1_Q = deque()
BEACON2_Q = deque()
BEACON3_Q = deque()

# Creating array to store pas values and generate the moving average of the RSSI values
PAST_BEACON1_RSSI = [0, 0, 0]
PAST_BEACON2_RSSI = [0, 0, 0]
PAST_BEACON3_RSSI = [0, 0, 0]

current_dog_coordinates = {'x': 0, 'y': 0}
dog_moving_status_subscriber = client.Client()
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

        if publish_dog_coordinates:
            dog_moving_status_subscriber.publish(topic_position, current_dog_coordinates)

        """
        nearby_distance = calculate_eucleadian_distance(current_dog_coordinates['x'], current_dog_coordinates['y'],
                                                       TRASH_CAN_X_COORDINATE, TRASH_CAN_Y_COORDINATE)
        if trashcan_nearby(nearby_distance, TRASH_CAN_THRESHOLD):
            dog_moving_status_subscriber.publish(topic_send, "DogNearBy")
            print("Dog is near the trash can")
        else:
            dog_moving_status_subscriber.publish(topic_send, "")
        """

def get_radius(TxPower, RSSI_values):
    distances = []

    d3 = calculate_distance(TxPower, RSSI_values[2])
    d2 = calculate_distance(TxPower, RSSI_values[1])
    d1 = calculate_distance(TxPower, RSSI_values[0])

    if RSSI_values[0] != 0:
        distances.append(d1)

    if RSSI_values[1] != 0:
        distances.append(d2)

    if RSSI_values[2] != 0:
        distances.append(d3)

    radius = sum(distances)/len(distances)

    return radius
    

def beacon1_callback(bt_addr, rssi, packet, additional_info):
    global BEACON1_TXPOWER, PAST_BEACON1_RSSI

    BEACON1_TXPOWER = int(packet.tx_power)

    BEACON1_RSSI = rssi

    PAST_BEACON1_RSSI[2] = PAST_BEACON1_RSSI[1]
    PAST_BEACON1_RSSI[1] = PAST_BEACON1_RSSI[0]
    PAST_BEACON1_RSSI[0] = BEACON1_RSSI

    r1 = get_radius(BEACON1_TXPOWER, PAST_BEACON1_RSSI)

    BEACON1_Q.append(r1)

    calculate_dog_position()


def beacon2_callback(bt_addr, rssi, packet, additional_info):
    global BEACON2_TXPOWER, PAST_BEACON2_RSSI

    BEACON2_TXPOWER = int(packet.tx_power)

    BEACON2_RSSI = rssi

    PAST_BEACON2_RSSI[2] = PAST_BEACON2_RSSI[1]
    PAST_BEACON2_RSSI[1] = PAST_BEACON2_RSSI[0]
    PAST_BEACON2_RSSI[0] = BEACON2_RSSI

    r2 = get_radius(BEACON1_TXPOWER, PAST_BEACON1_RSSI)

    BEACON2_Q.append(r2)

    calculate_dog_position()


def beacon3_callback(bt_addr, rssi, packet, additional_info):
    global BEACON3_TXPOWER, PAST_BEACON3_RSSI

    BEACON3_TXPOWER = int(packet.tx_power)

    BEACON3_RSSI = rssi

    PAST_BEACON3_RSSI[2] = PAST_BEACON3_RSSI[1]
    PAST_BEACON3_RSSI[1] = PAST_BEACON3_RSSI[0]
    PAST_BEACON3_RSSI[0] = BEACON3_RSSI

    r3 = get_radius(BEACON1_TXPOWER, PAST_BEACON1_RSSI)

    BEACON3_Q.append(r3)

    calculate_dog_position()


def on_message(client, userdata, message):
    global publish_dog_coordinates, current_dog_coordinates
    dog_moving_status = str(message.payload.decode("utf-8"))
    if dog_moving_status == "DogMoving":
        client.publish(topic_position, current_dog_coordinates)
        publish_dog_coordinates = True
    elif dog_moving_status == "DogStill":
        publish_dog_coordinates = False


def main():
    BEACON1_scanner = BeaconScanner(callback=beacon1_callback,
                                    filter=EddystoneFilter(namespaces=BEACON1_NAMESPACE)
                                    )

    BEACON2_scanner = BeaconScanner(callback=beacon2_callback,
                                    filter=EddystoneFilter(namespaces=BEACON2_NAMESPACE)
                                    )

    BEACON3_scanner = BeaconScanner(callback=beacon3_callback,
                                    filter=EddystoneFilter(namespaces=BEACON3_NAMESPACE)
                                    )

    dog_moving_status_subscriber.on_message = on_message
    dog_moving_status_subscriber.connect(BROKER, port=PORT, keepalive=KEEP_ALIVE)
    dog_moving_status_subscriber.loop_start()
    dog_moving_status_subscriber.subscribe(topic_subscribe)

    while True:
        BEACON1_scanner.start()
        BEACON2_scanner.start()
        BEACON3_scanner.start()

        # if len(BEACON1_Q) > 0 and len(BEACON2_Q) > 0 and len(BEACON3_Q) > 0:
        #     r1 = BEACON1_Q.popleft()
        #     r2 = BEACON2_Q.popleft()
        #     r3 = BEACON3_Q.popleft()
        #
        #     current_coordinates = get_coordinates(BEACON1_X_COORDINATE, BEACON2_X_COORDINATE, BEACON3_X_COORDINATE,
        #                                           BEACON1_Y_COORDINATE, BEACON2_Y_COORDINATE, BEACON3_Y_COORDINATE, r1,
        #                                           r2, r3)
        #
        #     """
        #     if dog is still and not moving:
        #         publish the coordinates to the topic "DogCoordinates" via MQTT
        #
        #         also print published coordinates to the topic "DogCoordinates"
        #     """
        #     mqtt_dog_publisher.publish(topic_position, current_coordinates)

            # nearby_distace = calculate_eucleadian_distance(current_dog_coordinates['x'], current_dog_coordinates['y'],
            #                                                TRASH_CAN_X_COORDINATE, TRASH_CAN_Y_COORDINATE)

            # if trashcan_nearby(nearby_distace, TRASH_CAN_THRESHOLD):
            #     mqtt_dog_publisher.publish(topic_send, "DogNearBy")
            #     print("Dog is near the trash can")
            # else:
            #     mqtt_dog_publisher.publish(topic_send, "")

        """
        if trashcan is moving:
            publish "DogPlayingWithTrashCan" to the topic "TrashCanInDanger" via MQTT
        else:
            publish "DogNotNearTrashCan" to the topic "TrashCanInDanger" via MQTT  

        
        if (avg_mag > threshold) & (status == "Idle"):
            status = "Bumped"
            # Publish status
            mqtt_dog_publisher.publish(topic_send, "DogPlayingWithTrashCan")
            print("Trashcan Bumped")
            time.sleep(3)
        elif (avg_mag < threshold) & (status == "Bumped"):
            status = "Idle"
            mqtt_dog_publisher.publish(topic_send, "DogNotNearTrashCan")

            # Publish status
            print("Trashcan not moving")
        """

        time.sleep(TIMEOUT)


if __name__ == '__main__':
    main()
