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


#Each of the four spinning lidar sensor nodes
#gets passed the specific i2c channel it is meant to
#use through the local param in the launch file as 
#a hex string '0x3A' for example, must convert to 
#an int





class IR(object):
    """A class that reads, analyzes, and publishes IR sensor data.

    Publisher:
    /pidrone/lidar_sensor
    /pidrone/heartbeat/infrared  #TODO rename all IR instances to either
    lidar or rangefinder on case by case basis
    """
    ### this block is to set up the lidar range finders
    # sys.path.insert(0, "build/lib.linux-armv7l-2.7/")
    ### the try/except block is to allow compatibility
    ### with the drones that use IR sensors
    

    def __init__(self, i2c, max_range):
        self.max_range = max_range

        ### development smoother
        GPIO.setmode(GPIO.BCM)
        mode = GPIO.getmode()
        #then innit the first one
        self.tof = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=i2c)
        self.tof.open()
        self.tof.start_ranging(1)
        #this is to increase frequency
        budget = 1
        inter = 1
        self.tof.set_timing(budget, inter)
        ### end of setup block

    def get_range(self):
        """need to convert from mm to meters"""
        self.distance = self.tof.get_distance() / 1000.0


    def publish_range(self, input_range):
        """Create and publish the Range message to publisher."""
        msg = Range()
        msg.max_range = self.max_range #different max for lidar version
        msg.min_range = 0.0   #range in meters
        msg.range = input_range
        msg.header.frame_id = "base"
        msg.header.stamp = rospy.Time.now()
        self.range_pub.publish(msg)

    def ctrl_c_handler(self, signal, frame):
        """Gracefully quit the infrared_pub node"""
        print "\nCaught ctrl-c! Stopping node."
        sys.exit()

def main():
    """Start the ROS node, create the publishers, and continuosly update and
    publish the lidar sensor data"""

    # ROS Setup
    ###########
    node_name = os.path.splitext(os.path.basename(__file__))[0]
    rospy.init_node(node_name)

    print rospy.get_param_names(), "NAMES"
    i2c= rospy.get_param("~i2cchannel")
    i2c= int(i2c, 16)
    max_range= rospy.get_param("/maxrange")
    max_range= float(max_range)

    #convert i2c channel from hex string to int

    # create IR object
    ir = IR(i2c, max_range)

    # Publishers
    ############
    ir.range_pub = rospy.Publisher('/pidrone/lidar_sensor', Range, queue_size=1)
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
        r.sleep()



if __name__ == "__main__":
    main()
