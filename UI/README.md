# IoT_Smart_Dog_Collar

## Description
This folder contains the necessary files for running the webpage UI to view the Smart Dog Collar status

## Environment
- Python 3.7.3
- nodejs v12.22.12

## Requirements
### Software
- Python3 3.7.3
- nodejs v12.22.12
- mosquitto

*Confim all setup instructions*
```
pip install nodejs
```

### Hardware
Server can be hosted on a raspberry pi or linux laptop using the provided methods

## Procedure
- Complete setup steps above
- From the *project*/UI folder, run:
```
node server.js
```
This will start the nodejs webserver on your localhost using port 8080

Environment:
- Raspberry pi
- nodejs

Setup:
- Copy SDC.conf to /etc/mosquitto/conf.d/
  Note: This may require permissions, if needed, use "sudo nano /etc/mosquitto/conf.d/SDC.conf" and copy the contents of the SDC.conf file to here
- Restart mosquitto using "sudo service mosquitto restart"
- Confirm mosquitto listening on port 1883 (normal mqtt) and port 9001 (websockets) using "sudo netstat -tlnpu | grep mosq"
- From project/UI/ folder, start webserver using "node server.js"
- Access site using http://localhost:8080

To use:
- Ensure ip is set correctly for MQTT (currently set for 'localhost')
- To topic 'pathPoints', send a string in JSON format containing x and y elements. Ex: "{"x": 10, "y": 20}"
  - This will be parsed by webpage and have a point plotted along with a connecting segment to the previous point if it     exists
