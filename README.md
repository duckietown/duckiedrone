# Template: template-ros

This template provides a boilerplate repository
for developing ROS-based software in Duckietown.

**NOTE:** If you want to develop software that does not use
ROS, check out [this template](https://github.com/duckietown/template-basic).


## How to use it

### 1. Fork this repository

Use the fork button in the top-right corner of the github page to fork this template repository.


### 2. Create a new repository

Create a new repository on github.com while
specifying the newly forked template repository as
a template for your new repository.


### 3. Define dependencies

List the dependencies in the files `dependencies-apt.txt` and
`dependencies-py.txt` (apt packages and pip packages respectively).


### 4. Place your code

Place your ROS packages in the directory `/packages` of
your new repository.

**NOTE:** Do not use absolute paths in your code,
the code you place under `/packages` will be copied to
a different location later.


### 5. Setup the launchfile

Change the file `launch.sh` in your repository to
launch your code.
=======
# dt-duckiebot-interface

Status:
[![Build Status](http://build-arm.duckietown.org/job/Docker%20Autobuild%20-%20dt-duckiebot-interface/badge/icon.svg)](http://build-arm.duckietown.org/job/Docker%20Autobuild%20-%20dt-duckiebot-interface/)
[![Docker Hub](https://img.shields.io/docker/pulls/duckietown/dt-duckiebot-interface.svg)](https://hub.docker.com/r/duckietown/dt-duckiebot-interface)

Repository containing all the necessary drivers to start sensors and actuators.
It should not contain any high-level functionality.

## How to launch manually

```$ docker -H <Hostname>.local run --name duckiebot-interface -v /data:/data --privileged --network=host -dit --restart unless-stopped -e ROBOT_TYPE=<ROBOT_TYPE> duckietown/duckiebot-interface:daffy-arm32v7```

By default, `ROBOT_TYPE` is duckiebot, and you can set it to watchtower or traffic_light if you use them.
