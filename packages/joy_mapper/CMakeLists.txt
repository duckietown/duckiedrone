cmake_minimum_required(VERSION 2.8.3)
project(joy_mapper)

find_package(catkin REQUIRED COMPONENTS
  rospy
  geometry_msgs
  std_msgs
  message_generation
)

add_message_files(
  FILES
  RC.msg
  Mode.msg
)

generate_messages(
  DEPENDENCIES
  std_msgs
)

catkin_package(CATKIN_DEPENDS message_runtime)


