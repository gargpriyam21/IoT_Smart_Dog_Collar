import time
import statistics

from beacontools import BeaconScanner, EddystoneTLMFrame, EddystoneFilter
from triangulation import *

rssi_avg = []
cnt = 0

def callback(bt_addr, rssi, packet, additional_info):
    global rssi_avg, cnt
    print("<%s, %d> %s %s" % (bt_addr, rssi, packet, additional_info))
        
    distance = calculate_distance(-65,rssi
    cnt += 1
    rssi_avg.append(distance)


# scan for all TLM frames of beacons in the namespace "12345678901234678901"
scanner = BeaconScanner(callback,
    # remove the following line to see packets from all beacons
    # device_filter=EddystoneFilter(namespace="12345678912345678913"),
    device_filter=EddystoneFilter(namespace="12345678912345678912"),
#    packet_filter=EddystoneTLMFrame
)
scanner.start()
time.sleep(100)
scanner.stop()
print(rssi_avg,cnt)
print(statistics.median(rssi_avg))



#19.952623149688797 + 28.183829312644534/2
# 25.118864315095795 + 15.848931924611133/2
# 11.220184543019636 + 5.623413251903491/2