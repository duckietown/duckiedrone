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
# if it fails to find the lidar hardware it will exit with error code 1 and
# based on the error code either the lidar or the infrared node will be run
if [ "${DEBUG}" = "1" ]; then echo "Rangefinder setup..."; fi
python2 $CODE_DIR/packages/pidrone_pkg/scripts/rangefinder_setup.py
rangefinder_status=$?
if [ "${DEBUG}" = "1" ];
then echo rangefinder_setup exit code $rangefinder_status; fi
if [ "${DEBUG}" = "1" ]; then echo "Done!"; fi


#Calibrate Accelerometer on startup (drone must be level)
if [ "${DEBUG}" = "1" ]; then echo "Calibrating Accelerometer..."; fi
python2 $CODE_DIR/packages/pidrone_pkg/scripts/calibrateAcc.py
if [ "${DEBUG}" = "1" ]; then echo "Done!"; fi


# launching rangefinder
if [ $rangefinder_status -eq 0 ] 
then rangefinderlaunch="lidar.launch"
echo dt_exec_roslaunch_pidrone_pkg_lidar.launch
fi

if [ $rangefinder_status -eq 10 ]
then rangefinderlaunch="infrared.launch"
echo dt_exec_roslaunch_pidrone_pkg_infrared.launch
fi

#launching app
#dt_exec roslaunch pidrone_pkg $rangefinderlaunch
dt_exec roslaunch pidrone_pkg drone.launch

#Choose range finder based on 

# ----------------------------------------------------------------------------
# YOUR CODE ABOVE THIS LINE

# terminate launch file
dt_launchfile_terminate
