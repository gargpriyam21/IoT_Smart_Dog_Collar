# IoT_Final_Group11

This repository is created for the sole purpose of uploading codes related to the Assignment 3 for the course CSC 591 - 022 Internet of Things: Architectures, Applications, and Implementation Spring 2022 of North Carolina State University.

## Environment
- macOS Monterey Version 12.2.1
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

## Procedure
### Setup broker to accept external connections
- Open the mosquitto config file located at /usr/local/etc/mosquitto.conf
  - Change `listener` to `listener 1883`
  - On the next lines add the following tree lines:-
    - protocol mqtt
    - listener 9001
    - protocol websockets
  - change `allow_anonymous` to `allow_anonymous true`
- Expose the the laptop ip address and port for connecting external devices on different networks.

Run the ***broker*** by executing the below command on a new terminal window
```
/usr/local/sbin/mosquitto -c /usr/local/etc/mosquitto/mosquitto.conf
```

Initially update the `BROKER_IP_ADDRESS` and `PORT`in the code file (*laptop.py*) to the IP_ADDRESS and PORT of device where the Broker is currently running. If the broker is on the same device update the value of BROKER_IP_ADDRESS to **'localhost'** and PORT to **'1883'**

Run the code (this will only be subscriber) code by executing the below command on a new terminal window
```
python3 laptop.py
```

The terminal will print messages from the following topics 
```
["ncsu/iot/DogWalkingStatus", "ncsu/iot/TrashCanInDanger", "ncsu/iot/DogCoordinates", "ncsu/iot/InformTrashcanOwner"]
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
