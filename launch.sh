#!/bin/bash

source /environment.sh

# initialize launch file
dt_launchfile_init

# YOUR CODE BELOW THIS LINE
# ----------------------------------------------------------------------------

# NOTE: Use the variable CODE_DIR to know the absolute path to your code
# NOTE: Use `dt_exec COMMAND` to run the main process (blocking process)

# Range finder setup
# if using lidar this will remap the i2c channels so that each of the 4
# sensors is on it's own channel and exit with error code zero
# if it fails to find the lidar hardware it will exit with error code 10 and
# based on the error code either the lidar or the infrared node will be run
if [ "${DEBUG}" = "1" ]; then echo "Rangefinder setup..."; fi
set +e
python2 $CODE_DIR/packages/rangefinder/src/rangefinder_setup.py 
rangefinder_status=$? #catch the error code
set -e
if [ "${DEBUG}" = "1" ]
then 
	echo rangefinder_setup exit code $rangefinder_status
fi
if [ "${DEBUG}" = "1" ]; then echo "Done!"; fi


# Determine rangefinder availibility
if [ $rangefinder_status -eq 0 ] 
then 
	rangefinderlaunch="lidar"
fi

if [ $rangefinder_status -eq 10 ]
then 
	rangefinderlaunch="infrared"
fi


#Calibrate Accelerometer on startup (drone must be level)
if [ "${DEBUG}" = "1" ]; then echo rangefinderlaunch $rangefinderlaunch; fi


#Calibrate Accelerometer on startup (drone must be level)
if [ "${DEBUG}" = "1" ]; then echo "Calibrating Accelerometer..."; fi
python2 $CODE_DIR/packages/flight_controller/src/calibrateAcc.py
if [ "${DEBUG}" = "1" ]; then echo "Done!"; fi



#launching app
dt_exec roslaunch duckiedrone_interface all_drivers.launch \
        veh:=$VEHICLE_NAME \
	robot_type:="duckiedrone" \
        rangefinder:=$rangefinderlaunch 

# ----------------------------------------------------------------------------
# YOUR CODE ABOVE THIS LINE

# terminate launch file
dt_launchfile_terminate
