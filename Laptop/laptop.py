import os
import sys
import time
from datetime import datetime
import statistics
import collections
from collections import defaultdict
from paho.mqtt import client as mqtt

# BROKER IP: Need to change if the broker is changed
BROKER_IP_ADDRESS = '192.168.1.163'
PORT = 1883
KEEPALIVE = 60
MQTT_TOPICS = [("ncsu/iot/DogWalkingStatus",2), ("ncsu/iot/TrashCanInDanger",2), ("ncsu/iot/DogCoordinates",2)]


def on_connect(client, userdata, flags, rc):
    print("Connected to the Broker with result code "+str(rc))

def on_message(client, userdata, message):
    TOPIC = message.topic
    QOS = message.qos

    TIMESTAMP = datetime.now().strftime("%d/%m/%Y %H:%M:%S %p")
    MESSAGE_SENT = str(message.payload.decode("utf-8"))

    print(TIMESTAMP + ": Received Message from - '" + TOPIC + " : " + MESSAGE_SENT)
    
    print("\n")
    print("BREAK".center(100, "-"))
    print("\n")

def run():
    
    subscriber = mqtt.Client("Laptop2")
    
    subscriber.on_connect = on_connect
    subscriber.on_message = on_message

    subscriber.connect(host = BROKER_IP_ADDRESS, port = PORT, keepalive = KEEPALIVE)

    subscriber.loop_start()

    subscriber.subscribe(MQTT_TOPICS)

    while True:
        continue

if __name__ == '__main__':
    run()