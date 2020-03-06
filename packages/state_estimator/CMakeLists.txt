cmake_minimum_required(VERSION 2.8.3)
project(state_estimator)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  geometry_msgs
  std_msgs
  nav_msgs
  sensor_msgs
  message_generation
)

add_message_files(
  FILES
  StateGroundTruth.msg
  UkfStats.msg
)

generate_messages(
  DEPENDENCIES
  geometry_msgs
  std_msgs
  nav_msgs
  sensor_msgs
)
catkin_package(CATKIN_DEPENDS message_runtime)


