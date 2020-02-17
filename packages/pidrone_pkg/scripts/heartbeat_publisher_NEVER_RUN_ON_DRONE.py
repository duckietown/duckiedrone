#!/usr/bin/env python

#The hearbeat that this node publishes is a signal to the drone that
#you can still make contact with the drone. therefore in order for this to work
#the heartbeat must be transmitted over the same channels that the commands are sent through.

#this is to replace the dependance on the web interface. 


#IMPORTANT 
#This
#should be run on the laptop you are using to control the drone. 
#Never on the drone itself.


import rospy
import platform
from std_msgs.msg import Empty


'''
publisher:
    /pidrone/heartbeat/web_interface #todo: change web_interface name
'''


def main():
    
    
    rospy.init_node("heartbeat_publisher_NEVER_RUN_ON_DRONE")
    heartbeat_pub = rospy.Publisher('/pidrone/heartbeat/web_interface', Empty, queue_size=1)
    r = rospy.Rate(10)


    while not rospy.is_shutdown():
        heartbeat_pub.publish(Empty())
        r.sleep()


if __name__ == "__main__":
    print "Under no circumstances should this node be running on a drone"
    if platform.machine()[:3] == 'arm':
        print "Heartbeat node is running on ARM architecture, shuting down"
        exit()
    else:
        main()
