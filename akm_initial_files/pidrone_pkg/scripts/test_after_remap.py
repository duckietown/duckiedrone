#!/usr/bin/env python
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably \
      because you need superuser privileges.  You can \
      achieve this by using 'sudo' to run your script")
import sys
sys.path.insert(0, "build/lib.linux-armv7l-2.7/")

import VL53L1X
import time
from datetime import datetime
import numpy as np
GPIO.setmode(GPIO.BCM)
mode = GPIO.getmode()
print(mode)
#GPIO.setup([4,17,18,27], GPIO.OUT)

#then innit the first one
tof1 = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x30)
tof1.open()

tof2 = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x31)
tof2.open()

tof3 = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x32)
tof3.open()

tof4 = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x33)
tof4.open()

print("Python: Initialized")

print("Python: Opened")

tof1.start_ranging(1)
tof2.start_ranging(1)
tof3.start_ranging(1)
tof4.start_ranging(1)

lidar_file = open("time_series_lidar{}.txt".format(datetime.utcnow().strftime("%H.%M")), 'w')

try:
    for i in range(1000):
        d1 = tof1.get_distance()
        #print("1 Time: {} Distance: {}mm".format(datetime.utcnow().strftime("%S.%f"), distance_mm))
        tof2.start_ranging(1)
        d2 = tof2.get_distance()
        #print("2 Time: {} Distance: {}mm".format(datetime.utcnow().strftime("%S.%f"), distance_mm))
        tof3.start_ranging(1)
        d3 = tof3.get_distance()
        tof4.start_ranging(1)
        d4 = tof4.get_distance()
        print("Time: {} Distance: \t{}\t{}\t{}\t{}".format(datetime.utcnow().strftime("%S.%f"), d1,d2,d3,d4))
	lidar_file.write("{} {} {} {} {}\n".format(datetime.utcnow().strftime("%M.%S.%f"), d1,d2,d3,d4))

except KeyboardInterrupt:
    tof1.stop_ranging()
    tof2.stop_ranging()
    tof3.stop_ranging()

lidar_file.close()
