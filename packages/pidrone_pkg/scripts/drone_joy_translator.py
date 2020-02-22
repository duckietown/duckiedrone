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

modepub = rospy.Publisher('/pidrone/desired/mode', Mode, queue_size=1)

positionPub = rospy.Publisher('/pidrone/position_control', Bool, queue_size=1)
positionControlPub = rospy.Publisher('/pidrone/desired/pose', Pose, queue_size=1)

velocityControlPub = rospy.Publisher('/pidrone/desired/twist', Twist, queue_size=1)

mappub = rospy.Publisher('/pidrone/map', Empty, queue_size=1)

resetpub = rospy.Publisher('/pidrone/reset_transform', Empty, queue_size=1)
togglepub = rospy.Publisher('/pidrone/toggle_transform', Empty, queue_size=1)
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


    def publishResetTransform():
        resetpub.publish(Empty())
    
    def publishToPosition():
        positionMsg.data = True
        positionPub.publish(positionMsg)

    def publishToVelocity():
        positionMsg.data = False
        positionPub.publish(positionMsg)

    def publishToggleMap():
        mappub.publish(Empty())

    def publishArm():
        if (positionMsg.data == False):
            poseMsg.position.x = 0.0
            poseMsg.position.y = 0.0
            poseMsg.position.z = 0.0
            positionControlPub.publish(poseMsg)
        else:
            twistMsg.linear.x = 0.0
            twistMsg.linear.y = 0.0
            twistMsg.linear.z = 0.0
            velocityControlPub.publish(twistMsg)
        if modeMsg.mode == "DISARMED":
            modeMsg.mode = "ARMED"
            modepub.publish(modeMsg)

    def publishDisarm():
        if (positionMsg.data == False):
            poseMsg.position.x = 0.0
            poseMsg.position.y = 0.0
            poseMsg.position.z = 0.0
            positionControlPub.publish(poseMsg)
        else:
            twistMsg.linear.x = 0.0
            twistMsg.linear.y = 0.0
            twistMsg.linear.z = 0.0
            velocityControlPub.publish(twistMsg)
        
        modeMsg.mode = "DISARMED"
        modepub.publish(modeMsg)

    def publishTakeoff():
        if (positionMsg.data == False):
            poseMsg.position.x = 0.0
            poseMsg.position.y = 0.0
            poseMsg.position.z = 0.0
            positionControlPub.publish(poseMsg)
        else:
            twistMsg.linear.x = 0.0
            twistMsg.linear.y = 0.0
            twistMsg.linear.z = 0.0
            twistMsg.angular.z = 0.0
            velocityControlPub.publish(twistMsg)    
        
        modeMsg.mode = "FLYING"
        modepub.publish(modeMsg)

    def publishTranslateLeft(value):
        if (positionMsg.data == False):
            poseMsg.position.x = -0.1+value*0.1
            poseMsg.position.y = 0.0
            poseMsg.position.z = 0.0
            positionControlPub.publish(poseMsg)
        else:
            twistMsg.linear.x = -0.1+value*0.1
            twistMsg.linear.y = 0.0
            twistMsg.linear.z = 0.0
            velocityControlPub.publish(twistMsg)
                

    def publishTranslateRight(value):
        if (positionMsg.data == False):
            poseMsg.position.x = 0.1+value*0.1
            poseMsg.position.y = 0.0
            poseMsg.position.z = 0.0
            positionControlPub.publish(poseMsg)
        else:
            twistMsg.linear.x = 0.1+value*0.1
            twistMsg.linear.y = 0.0
            twistMsg.linear.z = 0.0
            twistMsg.angular.z = 0.0
            velocityControlPub.publish(twistMsg)

    def publishTranslateForward(value):
        if (positionMsg.data == False):
            poseMsg.position.x = 0.0
            poseMsg.position.y = 0.1+value*0.1
            poseMsg.position.z = 0.0
            positionControlPub.publish(poseMsg)
        else:
            twistMsg.linear.x = 0.0
            twistMsg.linear.z = 0.0
            twistMsg.linear.y = 0.1+value*0.1
            twistMsg.angular.z = 0.0
            velocityControlPub.publish(twistMsg)

    def publishTranslateBackward(value):
        if (positionMsg.data == False):
            poseMsg.position.x = 0.0
            poseMsg.position.y = -0.1+value*0.1
            poseMsg.position.z = 0.0
            positionControlPub.publish(poseMsg)
        else:
            twistMsg.linear.x = 0.0
            twistMsg.linear.z = 0.0
            twistMsg.linear.y = -0.1+value*0.1
            twistMsg.angular.z = 0.0
            velocityControlPub.publish(twistMsg)

    def publishTranslateUp(value):
        poseMsg.position.x = 0.0
        poseMsg.position.y = 0.0
        poseMsg.position.z = 0.05+value*0.05
        positionControlPub.publish(poseMsg)
        
    def publishTranslateDown(value):
        poseMsg.position.x = 0.0
        poseMsg.position.y = 0.0
        poseMsg.position.z = -0.05+value*0.05
        positionControlPub.publish(poseMsg)

    def publishYawLeft():
        #modeMsg.mode = "FLYING" #uncommented in original idk why AKM
        twistMsg.linear.x = 0.0
        twistMsg.linear.y = 0.0
        twistMsg.linear.z = 0.0
        twistMsg.angular.z = -50.0
        velocityControlPub.publish(twistMsg)

    def publishYawRight():
        #modeMsg.mode = "FLYING"
        twistMsg.linear.x = 0.0
        twistMsg.linear.y = 0.0
        twistMsg.linear.z = 0.0
        twistMsg.angular.z = 50.0
        velocityControlPub.publish(twistMsg)

    def publishZeroVelocity():
        twistMsg.linear.x = 0.0
        twistMsg.linear.y = 0.0
        twistMsg.linear.z = 0.0
        twistMsg.angular.z = 0.0
        velocityControlPub.publish(twistMsg)
    




    print "callback"

    #print dir(data)
    #if data.buttons[3] == 1:
    #    z_counter = (z_counter+1) % z_total_steps
    #    print 3, "Z Stepping", z_counter
    #    mode.mode = 5
    #    mode.x_velocity = 0
    #    mode.y_velocity = 0
    #    if z_counter > ((z_total_steps / 2) - 1):
    #        mode.z_velocity = -z_step
    #    else:
    #        mode.z_velocity = z_step
    #    print "mode", mode
    #    modepub.publish(mode)
    if data.buttons[0] == 1:
        print "button", 0
        print "publishResetTransform()"
        publishResetTransform()

    if data.buttons[6] == 1:
        print "botton", 6
        print "publishToPosition()"
        publishToPosition()

    if data.buttons[7] == 1:
        print "button", 7
        print "publishToVelocity()"
        publishToVelocity()

    if data.buttons[4] == 1:
        print "button", 4
        print "publishToggleMap()"
        publishToggleMap()

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

    if data.buttons[4] == 1:
        print "button", 4
        print "publishYawLeft()"
        publishYawLeft()

    if data.buttons[5] == 1:
        print "button", 5
        print "publishYawRight()"
        publishYawRight()

    print data.axes
    if np.abs(data.axes[0]) >= 0.3:
        print "Axes 0"
	value = data.axes[0]
        if data.axes[0] > 0:
            print "publishTranslateLeft(value), value: ", data.axes[0]
            publishTranslateLeft(value)
        else:
            print "publishTranslateRight(value), value: ", data.axes[0]
            publishTranslateRight(value)

    if np.abs(data.axes[1]) >= 0.3:
        print "Axes 1"
        value = data.axes[1]
        if value > 0:
            print "publishTranslateForward(value), value: ", value
            publishTranslateForward(value)
        else:
            print "publishTranslateBackward(value), value: ", value
            publishTranslateBackward(value)

    if np.abs(data.axes[3]) >= 0.3:
        print "Axes 3"
        value = data.axes[3]
        if value > 0:
            print "publishTranslateUp(value), value: ", value
            publishTranslateUp(value)
        else:
            print "publishTranslateDown(value), value: ", value
            publishTranslateDown(value)
    '''
    #elif data.buttons[6] == 1:
    #    # land
    #    mode.mode = 3
    #    print "mode", mode
    #    modepub.publish(mode)
    #elif data.buttons[7] == 1:
    #    # arm
    #    mode.mode = 0
    #    print "mode", mode
    #    modepub.publish(mode)
    #elif data.buttons[8] == 1:
    #    mode.mode = 5
    #    mode.x_velocity = -data.axes[2] * scalar
    #    mode.y_velocity = data.axes[3] * scalar
    #    mode.z_velocity = data.axes[1]
    #    mode.yaw_velocity = -200.0 * data.axes[0]
    #    print "mode", mode
    #    modepub.publish(mode)
    #elif data.buttons[9] == 1:
    #    # takeoff
    #    mode.mode = 2
    #    print "mode", mode
    #    modepub.publish(mode)
    # should be able to do these at the same time
    #if data.buttons[10] == 1:
    #    print "resetting transform"
    #    resetpub.publish(Empty())
    #if data.buttons[11] == 1:
    #    print "toggling transform"
    #    togglepub.publish(Empty())
    
    #   if data.buttons[12] == 0:
    #       mode.x_velocity = 0 
    #       mode.y_velocity = 0
    #       mode.z_velocity = 0
    '''
def main():
    node_name = os.path.splitext(os.path.basename(__file__))[0]
    rospy.init_node(node_name)
    rospy.Subscriber("/joy", Joy, joy_callback)
    rospy.spin()
    
    
if __name__ == "__main__":
    main()
