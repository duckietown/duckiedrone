from __future__ import division
import rospy
import numpy as np
# import picamera.array
from pidrone_pkg.msg import State
from geometry_msgs.msg import TwistStamped
from sensor_msgs.msg import Image
from cv_bridge import CvBridge


class AnalyzeFlow():
    ''' A class used for real-time motion analysis of optical flow vectors to
    obtain the planar and yaw velocities of the drone.

    For more information, read the following:
    http://picamera.readthedocs.io/en/release-1.10/api_array.html#picamera.array.PiMotionAnalysis
    '''

    def __init__(self, camera_wh):
        # self.image_pub = rospy.Publisher("/duckiedrone2/camera_node/image_pub_test", Image, queue_size=1)
        self.bridge = CvBridge()

        rospy.Subscriber("/duckiedrone2/camera_node/image/raw", Image, self.callback)

        self.camera_wh = camera_wh

        self.setup(camera_wh)

        self.cols = None
        self.rows = None

        self.altitude = 2

    def callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        # rows, cols, channels) = cv_image.shape
        # print(cv_image.shape)

        # try:
        #     self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
        # except CvBridgeError as e:
        #     print(e)

        self.write(cv_image)

    def setup(self, camera_wh):
        ''' Initialize the instance variables '''

        # flow variables
        self.max_flow = camera_wh[0] / 16.0 * camera_wh[1] / 16.0 * 2**7
        self.flow_scale = .165
        self.flow_coeff = 100 * self.flow_scale / self.max_flow # (multiply by 100 for cm to m conversion)

        # self.altitude = 0.0


        # ROS setup:
        ############
        # Publisher:
        self.twistpub = rospy.Publisher('/duckiedrone2/camera_node/twist', TwistStamped, queue_size=1)
        # Subscriber:
        rospy.Subscriber("/pidrone/state", State, self.state_callback)

    def write(self, b):
        if self.cols is None:
            width, height = self.camera_wh
            self.cols = ((width + 15) // 16) + 1
            self.rows = (height + 15) // 16
        self.analyse(b)
        return len(b)

    def analyse(self, a):
        ''' Analyze the frame, calculate the motion vectors, and publish the
        twist message. This is implicitly called by the

        a : an array of the incoming motion data that is provided by the
            PiMotionAnalysis api
        '''
        # signed 1-byte values
        x = a[0]
        y = a[1]

        # print(a.shape)

        # calculate the planar and yaw motions
        x_motion = np.sum(x) * self.flow_coeff * self.altitude
        y_motion = np.sum(y) * self.flow_coeff * self.altitude
        twist_msg = TwistStamped()
        twist_msg.header.stamp = rospy.Time.now()
        twist_msg.twist.linear.x = self.near_zero(x_motion)
        twist_msg.twist.linear.y = - self.near_zero(y_motion)

        # Update and publish the twist message
        self.twistpub.publish(twist_msg)

    def near_zero(self, n):
        return 0 if abs(n) < 0.001 else n

    def state_callback(self, msg):
        """
        Store z position (altitude) reading from State
        """
        self.altitude = msg.pose_with_covariance.pose.position.z
