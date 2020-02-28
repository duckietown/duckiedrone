#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Joy
import numpy as np
import os
from geometry_msgs.msg import Pose, Twist
from pidrone_pkg.msg import Mode, RC
from std_msgs.msg import Float32, Empty, Bool

z_total_steps = 24
#z_counter = (z_total_steps / 4) - 1
z_counter = -1
z_step = 5 # cm
scalar = 15
modeMsg = Mode()
modeMsg.mode = 'DISARMED'
positionMsg = Bool()
positionMsg.data = True
poseMsg = Pose()
twistMsg = Twist()

modepub = rospy.Publisher('desired/mode', Mode, queue_size=1)

#positionPub = rospy.Publisher('position_control', Bool, queue_size=1)
#positionControlPub = rospy.Publisher('desired/pose', Pose, queue_size=1)

#elocityControlPub = rospy.Publisher('desired/twist', Twist, queue_size=1)

#mappub = rospy.Publisher('map', Empty, queue_size=1)

#resetpub = rospy.Publisher('reset_transform', Empty, queue_size=1)
#togglepub = rospy.Publisher('toggle_transform', Empty, queue_size=1)
#rospy.set_param('joy/autorepeat_rate', 20)

def joy_callback(data):
    global scalar
    global modepub
    global modeMsg
    global resetpub
    global z_counter
    global z_step
    global z_total_steps
    global positionMsg
    global twistMsg
    cmdpub = rospy.Publisher('fly_commands', RC, queue_size=1)


    def publishResetTransform():
        resetpub.publish(Empty())
    

    def publishArm():

        if modeMsg.mode == "DISARMED":
            modeMsg.mode = "ARMED"
            modepub.publish(modeMsg)

    def publishDisarm():
        
        modeMsg.mode = "DISARMED"
        modepub.publish(modeMsg)

    def publishTakeoff():

        modeMsg.mode = "FLYING"
        modepub.publish(modeMsg)

    def publish_cmd(cmd):
        """Publish the controls to /pidrone/fly_commands """
        msg = RC()
        msg.roll = cmd[0]
        msg.pitch = cmd[1]
        msg.yaw = cmd[2]
        msg.throttle = cmd[3]
        print(cmd)
        cmdpub.publish(msg)


    
    print "callback"

    if data.buttons[1] == 1:
        print "button", 1
        print "publishArm()"
        publishArm()

    if data.buttons[2] == 1:
        print "button", 2
        print "publishDisarm()"
        publishDisarm()

    if data.buttons[3] == 1:
        print "button", 3
        print "publishTakeoff()"
        publishTakeoff()

 
    print data.axes
    if np.abs(data.axes[0]) >= 0.3:
        print "Axes 0"
        value = data.axes[0]
        if data.axes[0] > 0:
            roll = 1500 + data.axes[0]*roll_factor
    else:
        roll = 1500
            
        
    if np.abs(data.axes[1]) >= 0.3:
        print "Axes 1"
        value = data.axes[1]
        if data.axes[1] > 0:
            pitch = 1500 + data.axes[1]*pitch_factor
    else:
        pitch = 1500

    if np.abs(data.axes[3]) >= 0.3:
        print "Axes 2"
        value = data.axes[3]
        if data.axes[3] > 0:
            throttle = 1000 + data.axes[3]*throttle_factor
    else:
        throttle = 1000

    if np.abs(data.axes[4]) >= 0.3:
        print "Axes 3"
        value = data.axes[4]
        if data.axes[3] > 0:
            yaw = 1500 + data.axes[3]*yaw_factor
    else:
        yaw = 1500

    publish_cmd([roll, pitch, yaw, throttle])






def main():
    node_name = os.path.splitext(os.path.basename(__file__))[0]
    rospy.init_node(node_name)
    rospy.Subscriber("/joy", Joy, joy_callback)
    rospy.spin()
    
    
if __name__ == "__main__":
    main()
