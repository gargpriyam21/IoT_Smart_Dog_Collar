from mpu6050 import mpu6050
import numpy as np
import time

mpu = mpu6050(0x68)
threshold = 10 #must be above threshold to move dog from "idle" to "moving" state
IMU_SAMPLING_RATE = 0.01 #seconds

#Calibrate sensors to account for acceleration due to gravity
def calibrate(sensors):
    #get 5 samples from x,y and z coordinates
    x = np.zeros(5)
    y = np.zeros(5)
    z = np.zeros(5)
    for i in range(0,5):
        x[i] = sensors.get_accel_data().get('x')
        y[i] = sensors.get_accel_data().get('y')
        z[i] = sensors.get_accel_data().get('z')
        time.sleep(IMU_SAMPLING_RATE)
    x_offset = np.mean(x)
    y_offset = np.mean(y)
    z_offset = np.mean(z)
    return [x_offset,y_offset,z_offset]

def get_mag(sensor, offset):
    vals = [sensor.get_accel_data().get('x'), sensor.get_accel_data().get('y')]
    mag = 0
    for i in range(0,2):
        mag = mag + ((vals[i]-offset[i])**2)
    return np.sqrt(mag)


def main():
    mag = [0,0,0]
    status = "Idle"
    #Publish status
    offset = calibrate(mpu)
    while True:
        mag[2] = mag[1]
        mag[1] = mag[0]
        mag[0] = get_mag(mpu,offset)
        avg_mag = np.mean(mag)
        if (avg_mag > threshold) & (status == "Idle"):
            status = "Bumped"
            #Publish status
            print("Trashcan Bumped")
            time.sleep(3)
        elif (avg_mag < threshold) & (status == "Bumped"):
            status = "Idle"
            #Publish status
            print("Trashcan not moving")
            
        time.sleep(IMU_SAMPLING_RATE)
if __name__ == '__main__':
    main()
