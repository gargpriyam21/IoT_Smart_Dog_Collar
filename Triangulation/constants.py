# MQTT Constants
BROKER = '192.168.1.163'
PORT = 1883
KEEP_ALIVE = 100

topic_send = "ncsu/iot/TrashCanInDanger"

topic_position = "ncsu/iot/DogCoordinates"

topic_subscribe = "ncsu/iot/DogWalkingStatus"

## Namespace of the beacons to be scanned
BEACON1_NAMESPACE = "12345678912345678911"
BEACON2_NAMESPACE = "12345678912345678912"
BEACON3_NAMESPACE = "12345678912345678913"

## Beacon 1 coordinates
BEACON1_X_COORDINATE = 3.5
BEACON1_Y_COORDINATE = 4

## Beacon 2 coordinates
BEACON2_X_COORDINATE = 0
BEACON2_Y_COORDINATE = 0

## Beacon 3 coordinates
BEACON3_X_COORDINATE = 0
BEACON3_Y_COORDINATE = 6.6

# Initializing the Tx power for each beacon
BEACON1_TXPOWER = -65
BEACON2_TXPOWER = -65
BEACON3_TXPOWER = -65

# Defining the timeout for each data reading
TIMEOUT = 1