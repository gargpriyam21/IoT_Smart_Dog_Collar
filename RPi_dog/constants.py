move_threshold = 3 #must be above threshold to move dog from "idle" to "moving" state
idle_threshold = 2 #must be below threshold to move dog from "moving" to "idle" state
IMU_SAMPLING_RATE = 0.01 #seconds
BROKER = '192.168.1.163'
PORT = 1883
KEEP_ALIVE = 100

#TODO: Brendan
rest_val = 10

topic_send = "ncsu/iot/DogWalkingStatus"
