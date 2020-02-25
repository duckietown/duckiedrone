#!/usr/bin/env python
import os
import rospy
import numpy as np
from std_msgs.msg import Empty
from sensor_msgs.msg import Range
######Subscribers
# /pidrone/lidar_sensor   1 thru 4

######Publishers
# /pidrone/infrared     #todo rename /pidrone/rangefinder


#this node takes in the four lidar sensor data
#streams and outputs the average of the most recent
#four measurments 

#the purpose of this is to stop one sensor over a watchtower
#or other discontinous terrain to throw off the height estimation
class rangefinder_average():

    def __init__(self, publisher):
        self.ranges = np.array([0.0,0.0,0.0,0.0])
        self.range_index = 0
        self.publisher = publisher
        self.max_range = None
        self.min_range = None
        self.header = None

    def increment_index(self):
        self.range_index +=1
        self.range_index = self.range_index % 4

    def return_median(self):
        return np.median(self.ranges)

    def return_mean(self):
        return np.mean(self.ranges)

    def callback(self, range_msg):
        #read in data
        
        self.ranges[self.range_index] = range_msg.range
        self.increment_index()
        self.max_range = range_msg.max_range
        self.min_range = range_msg.min_range
        self.header = range_msg.header
        self.out_message()

    def out_message(self):
        msg = Range()
        msg.max_range = self.max_range
        msg.min_range = self.min_range
        msg.range = self.return_median()
        msg.header = self.header
        self.publisher.publish(msg)
	print "Last four ranges recived: ", np.around(self.ranges, 4), "\t\t\t\r"





def main():
    node_name = os.path.splitext(os.path.basename(__file__))[0]
    rospy.init_node(node_name)

    print("we are in main")

    rangefinder_pub = rospy.Publisher('/pidrone/infrared', Range, queue_size=1)
    print("publihser created")
    rangefinder = rangefinder_average(rangefinder_pub)
    rangefinder_sub = rospy.Subscriber('/pidrone/lidar_sensor', Range, rangefinder.callback)
    r = rospy.Rate(100)
    i = 0
    rospy.spin()
    #print "Four Most Recent Lidar Values"
    #while not rospy.is_shutdown():
    #    rangefinder.out_message()
    #    r.sleep()
    #    i +=1
    #    print np.around(rangefinder.ranges, 4), "\t\t\t\r",


if __name__ == "__main__":
    main()
