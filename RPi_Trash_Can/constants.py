BROKER = '192.168.1.163'
PORT = 1883

TRASH_CAN_TOPIC = "ncsu/iot/TrashCanInDanger"

topic_inform_trashcan = "ncsu/iot/InformTrashcanOwner"


# Initializing the Trash Can's X and Y coordinates
TRASH_CAN_X_COORDINATE = 0
TRASH_CAN_Y_COORDINATE = 0

# Defining the Threshold for the trash can nearby
TRASH_CAN_THRESHOLD = 0.5

threshold = 10 #must be above threshold to move dog from "idle" to "moving" state
IMU_SAMPLING_RATE = 0.01 #seconds