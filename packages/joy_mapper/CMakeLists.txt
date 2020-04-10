cmake_minimum_required(VERSION 2.8.3)
project(joy_mapper)

find_package(catkin REQUIRED COMPONENTS
  rospy
  geometry_msgs
  std_msgs
  duckietown_msgs
  sensor_msgs
)


catkin_package(CATKIN_DEPENDS message_runtime)


