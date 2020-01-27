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

GPIO.setmode(GPIO.BCM)
mode = GPIO.getmode()
print(mode)

GPIO.setup([4,17,18,27], GPIO.OUT)
GPIO.setup(4, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.output(4, GPIO.LOW)
GPIO.output(17, GPIO.LOW)
GPIO.output(18, GPIO.LOW)
GPIO.output(27, GPIO.LOW)
time.sleep(0.001)
GPIO.output(4, GPIO.HIGH)
GPIO.output(17, GPIO.HIGH)
GPIO.output(18, GPIO.HIGH)
GPIO.output(27, GPIO.HIGH)
#put all down except 4
GPIO.output(4, GPIO.LOW)
GPIO.output(17, GPIO.LOW)
GPIO.output(18, GPIO.LOW)
GPIO.output(27, GPIO.LOW)
#then innit the first one


GPIO.output(4, GPIO.HIGH)
tof1 = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)
tof1.open()
tof1.change_address(0x30)

tof1 = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x30)
tof1.open()



GPIO.output(17, GPIO.HIGH)
tof2 = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)
tof2.open()
tof2.change_address(0x31)
tof2 = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x31)
tof2.open()


GPIO.setup(18, GPIO.HIGH)
tof3 = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)
tof3.open()
tof3.change_address(0x32)
tof3 = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x32)
tof3.open()

GPIO.setup(27, GPIO.HIGH)
tof4 = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)
tof4.open()
tof4.change_address(0x33)
tof4 = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x33)
tof4.open()

print("Python: Initialized")

print("Python: Opened")
