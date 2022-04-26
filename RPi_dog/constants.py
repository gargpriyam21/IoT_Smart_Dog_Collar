move_threshold = 5 #must be above threshold to move dog from "idle" to "moving" state
idle_threshold = 4 #must be below threshold to move dog from "moving" to "idle" state
IMU_SAMPLING_RATE = 0.01 #delay in seconds between samples
BROKER = '192.168.1.163'
PORT = 1883
KEEP_ALIVE = 100

rest_val = 8 #approximate value of accel magnitude at rest

topic_send = "ncsu/iot/DogWalkingStatus"
