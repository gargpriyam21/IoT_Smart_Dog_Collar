import paho.mqtt.client as client
from mpu6050 import mpu6050
import numpy as np
import time
from constants import *

def main():
    trashCanClient = client.Client()
    trashCanClient.connect()

    client.Client()
    trashCanClient.connect(BROKER, port=PORT)

if __name__ == '__main__':
    main()