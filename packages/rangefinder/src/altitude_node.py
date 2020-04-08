#!/usr/bin/env python
import os
import rospy
import numpy as np
from std_msgs.msg import Empty
from sensor_msgs.msg import Range
from geometry_msgs.msg import Quaternion
from sensor_msgs.msg import Imu

import tf

######Subscribers
# /duckiedrone/lidar_sensor_node  1 thru 4
# /duckiedrone/infrared_node
# /duckiedrone/imu

######Publishers
# /duckiedrone/altitude     #todo rename /pidrone/rangefinder


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

        self.range_angle = 0 
        #angle between the direction the range finder is pointed (normal to the drone)
        #and the gravity vector (towards the ground)

    def update_angle(self, imu_msg):
        base = np.array([0,0,1,0])
        quat = imu_msg.orientation
        quaternion = np.array([quat.x, quat.y, quat.z, quat.w])
        quaternion_conjugate = np.array([-quat.x, -quat.y, -quat.z, quat.w])

        new = tf.transformations.quaternion_multiply(quaternion, \
              tf.transformations.quaternion_multiply(base, quaternion_conjugate))

        

        self.range_angle = np.arccos(np.dot(new[0:3], base[0:3]))


    def increment_index(self):
        self.range_index +=1
        self.range_index = self.range_index % 4

    def return_median(self):
        return np.median(self.ranges)

    def return_mean(self):
        return np.mean(self.ranges)

    def callback(self, range_msg):
        #read in data
        print np.around(range_msg.range,4), "\t\t\t", np.around(range_msg.range * np.cos(self.range_angle), 4)
        self.ranges[self.range_index] = range_msg.range * np.cos(self.range_angle)
        #project this along the verticle axis TODO: convert this to use frames
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
        self.publisher.heartbeat.publish(Empty())
	   #print "Last four ranges recived: ", np.around(self.ranges, 4), "\t\t\t\r"





def main():
    node_name = os.path.splitext(os.path.basename(__file__))[0]
    rospy.init_node(node_name)

    rangefinder_pub = rospy.Publisher('altitude', Range, queue_size=1)
    rangefinder_pub.heartbeat = rospy.Publisher('heartbeat/altitude', Empty, queue_size=1)

    rangefinder = rangefinder_average(rangefinder_pub)


    rospy.Subscriber('imu', Imu, rangefinder.update_angle)
    rospy.Subscriber('lidar_sensor_1', Range, rangefinder.callback)
    rospy.Subscriber('lidar_sensor_2', Range, rangefinder.callback)
    rospy.Subscriber('lidar_sensor_3', Range, rangefinder.callback)
    rospy.Subscriber('lidar_sensor_4', Range, rangefinder.callback)
    rospy.Subscriber('infrared_sensor', Range, rangefinder.callback)
    r = rospy.Rate(100)
    i = 0
    rospy.spin()



if __name__ == "__main__":
    main()
