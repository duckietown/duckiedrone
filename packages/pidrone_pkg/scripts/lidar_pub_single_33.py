#!/usr/bin/env python

import sys
import os
import rospy
import signal
import time
from std_msgs.msg import Empty
from sensor_msgs.msg import Range

import RPi.GPIO as GPIO
import VL53L1X


#in the future I intend to have one lidar_pub_single.py
#and be able to pass the i2c address, the dirty fix
#in the meantime is to hardcode the values and have
#four files
i2c=0x33


### this block is to set up the lidar range finders

# sys.path.insert(0, "build/lib.linux-armv7l-2.7/")


### the try/except block is to allow compatibility
### with the drones that use IR sensors
### it is kind of grubby but ideally it will make
### development smoother
GPIO.setmode(GPIO.BCM)
mode = GPIO.getmode()
#then innit the first one
tof = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=i2c)
tof.open()


tof.start_ranging(1)

#this is to increase frequency
budget = 1
inter = 1
tof.set_timing(budget, inter)
### end of setup block

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
        """need to convert from mm to meters"""
        self.distance = tof.get_distance() / 1000.0


    def publish_range(self, range):
        """Create and publish the Range message to publisher."""
        msg = Range()
        msg.max_range = 3.0 #different max for lidar version
        msg.min_range = 0   #range in meters
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
