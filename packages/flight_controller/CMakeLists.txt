cmake_minimum_required(VERSION 2.8.3)
project(flight_controller)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  geometry_msgs
  std_msgs
  nav_msgs
  sensor_msgs
  message_generation
)



## Generate messages in the 'msg' folder
add_message_files(
  FILES
  RC.msg
  Mode.msg
)


## Generate added messages and services with any dependencies listed here
generate_messages(
  DEPENDENCIES
  geometry_msgs
  std_msgs
  nav_msgs
  sensor_msgs
  geometry_msgs
)
catkin_package(CATKIN_DEPENDS message_runtime)

catkin_package()

include_directories(
  ${catkin_INCLUDE_DIRS}
)

