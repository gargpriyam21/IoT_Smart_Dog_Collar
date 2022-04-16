from mpu6050 import mpu6050
import numpy as np
import time

mpu = mpu6050(0x68)
move_threshold = 3 #must be above threshold to move dog from "idle" to "moving" state
idle_threshold = 0.5 #must be below threshold to move dog from "moving" to "idle" state
gyro_threshold = 100 #threshold to recalibrate MPU if dog rolls over
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

def get_rot(sensor):
	rot = [sensor.get_gyro_data().get('x'), sensor.get_gyro_data().get('y'), sensor.get_gyro_data().get('z')]
	return rot

def main():
	mag = [0,0,0]
	diff = np.zeros(3)
	status = "Idle"
	offset = calibrate(mpu)
	while True:
		mag[2] = mag[1]
		mag[1] = mag[0]
		mag[0] = get_mag(mpu,offset)
		avg_mag = np.mean(mag)
		for i in range(0,3):
			diff[i-3] = diff[i-2]
		diff[0] = mag[0] - avg_mag
		avg_diff = np.mean(diff)

		if (avg_diff > move_threshold) & (status == "Idle"):
			status = "Moving"
			print("Dog is moving")
		elif (avg_diff < idle_threshold) & (status == "Moving"):
			status = "Idle"
			print("Dog is idle")
		#publish status to dog topic
		time.sleep(IMU_SAMPLING_RATE)
		#print(avg_diff)
if __name__ == '__main__':
    main()
