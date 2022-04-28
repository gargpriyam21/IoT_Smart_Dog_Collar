# IoT_Final_Group11

This repository is created for the sole purpose of uploading codes related to the Final Project for the course CSC 591 - 022 Internet of Things: Architectures, Applications, and Implementation Spring 2022 of North Carolina State University.

## Environment
- Python 3.7.3

## Requirements
### Software
- Python3 3.7.3
- paho-mqtt v1.6.1
- numpy v1.19.5
- mosquitto 
- wiotp-sdk
- requests
- RPi.GPIO
- MATLAB

```
pip install requirements.txt
```

### Hardware
- x2 Raspberry Pi 3b
- x2 MPU6050 Accelerometer + gyro
- x3 Mobile phones with bluetooth

To setup the hardware, connect the following raspberry pi GPIO pins to the corresponding MPU pins.

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
