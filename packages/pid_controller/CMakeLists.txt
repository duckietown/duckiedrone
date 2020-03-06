cmake_minimum_required(VERSION 2.8.3)
project(pid_controller)

find_package(catkin REQUIRED COMPONENTS
  rospy
  geometry_msgs
  std_msgs
  nav_msgs
  sensor_msgs
)


catkin_package(CATKIN_DEPENDS message_runtime)


