# IoT Final Project Group11

This repository is created for the sole purpose of uploading codes related to the Final Project for the course CSC 591 - 022 Internet of Things: Architectures, Applications, and Implementation Spring 2022 of North Carolina State University.

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
- x2 Raspberry Pi 3b
- x2 MPU6050 Accelerometer + gyro
- x3 Mobile phones with bluetooth

To setup the hardware for both Pis, connect the following raspberry pi GPIO pins to the corresponding MPU pins.

GPIO 2 to SDA, <br />
GPIO 3 to SCL, <br />
5V to VCC, <br />
GND to GND <br />

## Procedure
To Track Dog's Status
1. Attach smart harness to dog
2. Setup up other raspberry pi on trashcan
3. ssh into both raspberry pis from a laptop
4. setup the three bluetooth beacons at locations inducated on UI
5. On the laptop, run the mqtt broker and the UI client
6. On the trashcan Pi, run trashCan.py in the RPi_Trash_Can folder
7. on the smart harness, run dogPub.py in the RPi_dog folder
8. next on the smart harness, run ble_detection.py in the Triangulation folder

Once everything is connected and running, the UI should display the status of the dog and trashcan, and should start plotting the coordinates it is calculating from the RSSI values.

To Graph MPU Data:
1. Attach smart harness to dog
2. run "python3 RPi_dog/dataCollect.py"
3. Follow along with prompts: Select task and name file
4. Have dog complete task
5. Program will end once dog remains still for 2-3 seconds
6. Move new files onto a seperate device which has MATLAB installed
7. run the MATLAB script "dogGraph.m"
8. Follow prompts: give file name and title for graph
9. Plot will be generated with accelerometer and gyro data

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
