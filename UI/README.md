This folder contains the necessary files for running the webpage to view the Smart Dog Collar status

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