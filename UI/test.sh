#! /bin/sh
mosquitto_pub -d -t "ncsu/iot/DogCoordinates" -m '{"x":50,"y":50}'
mosquitto_pub -d -t "ncsu/iot/DogCoordinates" -m '{"x":150,"y":150}'
mosquitto_pub -d -t "ncsu/iot/DogCoordinates" -m '{"x":250,"y":200}'
mosquitto_pub -d -t "ncsu/iot/DogCoordinates" -m '{"x":350,"y":150}'
mosquitto_pub -d -t "ncsu/iot/DogCoordinates" -m '{"x":450,"y":50}'
