#!/bin/bash

source /environment.sh

# initialize launch file
dt_launchfile_init

# YOUR CODE BELOW THIS LINE
# ----------------------------------------------------------------------------

#set i2c addresses for remapping and use by lidar nodes
i2c_address1="0x30"
i2c_address2="0x31"
i2c_address3="0x32"
i2c_address4="0x33"

# NOTE: Use the variable CODE_DIR to know the absolute path to your code
# NOTE: Use `dt_exec COMMAND` to run the main process (blocking process)

# Range finder setup
# if using lidar this will remap the i2c channels so that each of the 4
# sensors is on it's own channel and exit with error code zero
# if it fails to find the lidar hardware it will exit with error code 1 and
# based on the error code either the lidar or the infrared node will be run
if [ "${DEBUG}" = "1" ]; then echo "Rangefinder setup..."; fi
set +e
python2 $CODE_DIR/packages/pidrone_pkg/scripts/rangefinder_setup.py \
        --channels \
        $i2c_address1 $i2c_address2 $i2c_address3 \
        $i2c_address4

rangefinder_status=$?
set -e
if [ "${DEBUG}" = "1" ];
then echo rangefinder_setup exit code $rangefinder_status; fi
if [ "${DEBUG}" = "1" ]; then echo "Done!"; fi


# Determine rangefinder availibility
if [ $rangefinder_status -eq 0 ] 
then 
	rangefinderlaunch="lidar"
	maxrange="3.1"
fi

if [ $rangefinder_status -eq 10 ]
then 
	rangefinderlaunch="infrared"
	maxrange="0.65"
fi


#Calibrate Accelerometer on startup (drone must be level)
if [ "${DEBUG}" = "1" ]; then echo rangefinderlaunch $rangefinderlaunch; fi


#Calibrate Accelerometer on startup (drone must be level)
if [ "${DEBUG}" = "1" ]; then echo "Calibrating Accelerometer..."; fi
python2 $CODE_DIR/packages/pidrone_pkg/scripts/calibrateAcc.py
if [ "${DEBUG}" = "1" ]; then echo "Done!"; fi



#launching app
dt_exec roslaunch pidrone_pkg drone.launch rangefinder:=$rangefinderlaunch \
	maxrange:=$maxrange \
	i2c1:=$i2c_address1 i2c2:=$i2c_address2 i2c3:=$i2c_address3 \
	i2c4:=$i2c_address4


# ----------------------------------------------------------------------------
# YOUR CODE ABOVE THIS LINE

# terminate launch file
dt_launchfile_terminate
