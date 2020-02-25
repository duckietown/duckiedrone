#!/bin/bash

source /environment.sh

# initialize launch file
dt_launchfile_init

# YOUR CODE BELOW THIS LINE
# ----------------------------------------------------------------------------

#NOTE: Use the variable CODE_DIR to know the absolute path to your code
# NOTE: Use `dt_exec COMMAND` to run the main process (blocking process)


# launching app
dt_exec roslaunch pidrone_pkg drone.launch veh:=$VEHICLE_NAME \
	robot_type:=$ROBOT_TYPE
#this is where the node that communicates with the web browser is launched
dt_exec roslaunch pidrone_pkg rosbridge_websocket.launch
# ----------------------------------------------------------------------------
# YOUR CODE ABOVE THIS LINE

# terminate launch file
dt_launchfile_terminate
