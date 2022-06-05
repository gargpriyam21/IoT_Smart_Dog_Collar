# IoT_Smart_Dog_Collar
## Environment
- Python 3.7.3

## Requirements
### Software
- Python3 3.7.3
- paho-mqtt==1.6.1
- numpy==1.19.5
- mosquitto 
- wiotp-sdk
- requests==2.25.1
- RPi.GPIO==0.7.0
- MATLAB
- beacontools==2.1.0
- gattlib==0.20201113
- mpu6050-raspberrypi==1.2
- Pillow==8.1.2
- PyBluez==0.23
- requests-oauthlib==1.0.0
- responses==0.12.1
- sympy==1.10.1
- urllib3==1.26.5


Follow this [link](https://learn.adafruit.com/install-bluez-on-the-raspberry-pi/installation) and follow the steps to install Bluez

```
pip install requirements.txt
```

### Hardware
- x1 Raspberry Pi 3b
- x1 MPU6050 Accelerometer + gyro
- x1 Mobile phones with bluetooth

To setup the hardware for both Pis, connect the following raspberry pi GPIO pins to the corresponding MPU pins.

GPIO 2 to SDA, <br />
GPIO 3 to SCL, <br />
5V to VCC, <br />
GND to GND <br />


## Procedure
Setup a Mobile phones with bluetooth as BLE beacon near the trashcan and update the namespace of the beacon in the `Triangulation/constants.py`

Initially update the `BROKER` and `PORT`in the code file (*constants.py*) to the IP_ADDRESS and PORT of device where the Broker is currently running. If the broker is on the same device update the value of BROKER_IP_ADDRESS to **'localhost'** and PORT to **'1883'**

- To run from file location: 

```
python3 trashCan.py
```