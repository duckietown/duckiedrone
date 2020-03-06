#!/usr/bin/env python
import sys
import os
import rospy
# import picamera
from sensor_msgs.msg import Image
from analyze_flow import AnalyzeFlow
# from analyze_phase import AnalyzePhase
from cv_bridge import CvBridge


def main():
    resolution = (640, 480)
    flow_analyzer = AnalyzeFlow(resolution)
    rospy.init_node('analyze_flow_and_phase_node')
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")

    return


if __name__ == '__main__':
    main()
