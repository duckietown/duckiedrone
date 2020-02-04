#!/usr/bin/env python

import sys
import os
import rospy
import signal
import time
from std_msgs.msg import Empty
from sensor_msgs.msg import Range


### this block is to set up the lidar range finders
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably \
      because you need superuser privileges.  You can \
      achieve this by using 'sudo' to run your script")

# sys.path.insert(0, "build/lib.linux-armv7l-2.7/")
import VL53L1X
import numpy as np


### the try/except block is to allow compatibility
### with the drones that use IR sensors
### it is kind of grubby but ideally it will make
### development smoother
try:
    GPIO.setmode(GPIO.BCM)
    mode = GPIO.getmode()
    #then innit the first one
    tof1 = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x30)
    tof1.open()

    tof2 = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x31)
    tof2.open()

    tof3 = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x32)
    tof3.open()

    tof4 = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x33)
    tof4.open()

    tof1.start_ranging(1)
    tof2.start_ranging(1)
    tof3.start_ranging(1)
    tof4.start_ranging(1)

    #this is to increase frequency
    budget = 1
    inter = 1
    tof1.set_timing(budget, inter)
    tof2.set_timing(budget, inter)
    tof3.set_timing(budget, inter)
    tof4.set_timing(budget, inter)
except:
    print "Failed to start LIDAR sensors: Trying Infrared"
    os.system("python infrared_pub.py")
    exit()



### end of setup block
tofs = (tof1, tof2, tof3, tof4)
tof_index = 0
from datetime import datetime

class IR(object):
    """A class that reads, analyzes, and publishes IR sensor data.

    Publisher:
    /pidrone/infrared
    """

    def __init__(self):
        self.GAIN = 1
        self.distance = 0
        # values used to define the slope and intercept of
        # distance as a function of voltage : d(v) = 1/v * m + b
        self.m = 181818.18181818182 * 1.238
        self.b = -8.3 + 7.5

    def get_range(self):
        """Read the data from the LIDARs and update the distance and
        smoothed_distance values."""
        #d1 = tof1.get_distance()
        #d2 = tof2.get_distance()
        #d3 = tof3.get_distance()
        #d4 = tof4.get_distance()
        #median = np.median(np.array([d1,d2,d3,d4]), axis=0)
        #self.distance = median/1000.0
        global tof_index
        self.distance = tofs[tof_index].get_distance() / 1000.0
        tof_index = tof_index + 1
        tof_index = tof_index % 4
        #voltage = self.adc.read_adc(0, self.GAIN)
        #if voltage <= 0:
        #    voltage = 1
        #    print "ERROR: BAD VOLTAGE!!!"
        #self.distance = ((1.0 / voltage) * self.m + self.b) / 100.0 # 100 is for cm -> m

    def publish_range(self, range):
        """Create and publish the Range message to publisher."""
        msg = Range()
        msg.max_range = 0.8
        msg.min_range = 0
        msg.range = range
        msg.header.frame_id = "base"
        msg.header.stamp = rospy.Time.now()
        self.range_pub.publish(msg)

    def ctrl_c_handler(self, signal, frame):
        """Gracefully quit the infrared_pub node"""
        print "\nCaught ctrl-c! Stopping node."
        sys.exit()

def main():
    """Start the ROS node, create the publishers, and continuosly update and
    publish the IR sensor data"""

    # ROS Setup
    ###########
    node_name = os.path.splitext(os.path.basename(__file__))[0]
    rospy.init_node(node_name)

    # create IR object
    ir = IR()

    # Publishers
    ############
    ir.range_pub = rospy.Publisher('/pidrone/infrared', Range, queue_size=1)
    ir.heartbeat_pub = rospy.Publisher('/pidrone/heartbeat/infrared', Empty, queue_size=1)
    print 'Publishing IR'

    # Non-ROS Setup
    ###############
    # set the while loop frequency
    r = rospy.Rate(100)
    # set up the ctrl-c handler
    signal.signal(signal.SIGINT, ir.ctrl_c_handler)

    while not rospy.is_shutdown():
        ir.heartbeat_pub.publish(Empty())
        ir.get_range()
        ir.publish_range(ir.distance)



if __name__ == "__main__":
    main()
