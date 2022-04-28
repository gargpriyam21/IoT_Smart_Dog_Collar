# IoT Final Project Group11

This repository is created for the sole purpose of uploading codes related to the Final Project for the course CSC 591 - 022 Internet of Things: Architectures, Applications, and Implementation Spring 2022 of North Carolina State University.

## Environment
- Python 3.7.3

## Requirements
### Software
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
- x4 Mobile phones with bluetooth

To setup the hardware for both Pis, connect the following raspberry pi GPIO pins to the corresponding MPU pins. 

GPIO 2 to SDA, <br />
GPIO 3 to SCL, <br />
5V to VCC, <br />
GND to GND <br />

This code will be excuted on the same Raspberry Pi as that of the RPI_dog.


## Procedure

Place you 3 Mobile phones with bluetooth acting as the bluetooth beacons and chage the `NAMESPACE` and the `X_COORDINATE` and the `Y_COORDINATE` to the respective coordinate position of the beacons.

Initially update the `BROKER` and `PORT`in the code file (*constants.py*) to the IP_ADDRESS and PORT of device where the Broker is currently running. If the broker is on the same device update the value of BROKER_IP_ADDRESS to **'localhost'** and PORT to **'1883'**

- To run from file location: 

```
python3 ble_detection.py
```

# Instructor
- Dr. Muhammad Shahzad (mshahza@ncsu.edu )

# Teaching Assistants
- Hassan Ali Khan (hakhan@ncsu.edu)

# Team
- Priyam Garg (pgarg6@ncsu.edu)
- Divyang Doshi	(ddoshi2@ncsu.edu)
- Brendan Driscoll (bhdrisco@ncsu.edu)
- Jordan Boerger (jwboerge@ncsu.edu)
- Vishal Veera Reddy (vveerar2@ncsu.edu)
