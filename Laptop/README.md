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


```
brew install mosquitto
pip install paho-mqtt
pip install numpy
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
