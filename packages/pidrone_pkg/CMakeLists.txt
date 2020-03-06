cmake_minimum_required(VERSION 2.8.3)
project(pidrone_pkg)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  geometry_msgs
  std_msgs
  nav_msgs
)


catkin_package(CATKIN_DEPENDS message_runtime)

catkin_package(
)

include_directories(
  ${catkin_INCLUDE_DIRS}
  )
