cmake_minimum_required(VERSION 2.8.3)
project(duckiebot_interface)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  rospy
  duckietown_msgs
)

catkin_package(CATKIN_DEPENDS message_runtime)

catkin_package()

include_directories(
  ${catkin_INCLUDE_DIRS}
)
