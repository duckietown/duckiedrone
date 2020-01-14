ARG REPO_NAME="cleandrone"

ARG ARCH=arm32v7
FROM duckietown/dt-ros-commons:daffy-${ARCH}

MAINTAINER Arthur MacKeith <amackeith@uchicago.edu>

RUN echo "Hello!"
RUN rm -rf /etc/apt/*
ADD apt_from_drone /etc/apt/

RUN apt-get update 
RUN /usr/bin/apt-get --yes -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" install libraspberrypi0

RUN /usr/bin/apt-get --yes --force-yes -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" install libraspberrypi-bin
RUN /usr/bin/apt-get --yes --force-yes -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" install libraspberrypi-dev
RUN /usr/bin/apt-get --yes --force-yes -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" install libraspberrypi-doc
RUN /usr/bin/apt-get --yes --force-yes -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" install raspberrypi-bootloader 
RUN apt-get update
RUN sudo apt-get -y upgrade bluez-firmware linux-firmware pi-bluetooth


#this installs ping, vim, and sshfs
RUN apt-get update && apt-get install -y iputils-ping && apt-get install -y vim && apt-get install -y sshfs
RUN apt-get -y install lsb-core
RUN apt-get -y install screen
RUN apt-get -y install vim

RUN sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
RUN apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net:80 --recv-key 421C365BD9FF1F717815A3895523BAEEB01FA116
RUN apt-get update
RUN apt-get -y install ros-kinetic-rosbridge-suite --allow-unauthenticated

###okay up to here 

RUN apt-get -y install hostapd

RUN apt-get -y install dnsmasq

RUN apt-get -y install nmap

RUN apt-get -y install netcat

RUN apt-get -y install vnc4server

RUN apt-get -y upgrade hostapd --fix-missing

RUN apt-get -y upgrade

RUN apt-get -y install ros-kinetic-web-video-server

RUN apt-get -y install ros-kinetic-camera-info-manager

RUN apt-get -y install ros-kinetic-camera-info-manager-py

RUN apt-get -y install python-opencv

RUN apt-get -y install libopencv-dev

RUN apt-get -y install python-pip

RUN apt-get -y install gfortran libopenblas-dev liblapack-dev python-dev

RUN apt-get -y install gedit

RUN apt-get -y install camorama

RUN /usr/bin/apt-get -y -u dist-upgrade

#RUN /usr/bin/apt-get -y install ubuntu-minimal parted software-properties-common

#RUN /usr/bin/apt-get -y install ubuntu-standard

#RUN /usr/bin/apt-get -y install --no-install-recommends ubuntu-mate-core^

#RUN /usr/bin/apt-get -y install --no-install-recommends ubuntu-mate-desktop^

#RUN /usr/bin/apt-get -y install --no-install-recommends oem-config-gtk ubiquity-frontend-gtk ubiquity-ubuntu-artwork

#RUN /usr/bin/apt-get -y install --no-install-recommends oem-config-slideshow-ubuntu-mate

RUN /usr/bin/apt-get -y install openssh-server sshguard

RUN apt-get update 
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install keyboard-configuration
RUN /usr/bin/apt-get -y install xserver-xorg-video-fbturbo


RUN apt-get -y install libpcre3 fonts-freefont-ttf fbset libpcre3-dev
#RUN apt-get -y install libpcrecpp0 
RUN apt-get -y install libva-dev libva-x11-1 libva1


####
#RUN apt-get update -y && apt-get -y install wget ca-certificates libpcre3 libfreetype6 fonts-freefont-ttf dbus libssl1.0.0 libsmbclient libssh-4 fbset libraspberrypi0
#RUN wget https://archive.raspberrypi.org/debian/pool/main/o/omxplayer/omxplayer_0.3.6~git20160102~f544084_armhf.deb
#RUN dpkg -i  omxplayer_0.3.6~git20160102~f544084_armhf.deb
####


#RUN wget http://omxplayer.sconde.net/builds/omxplayer_0.2.4~git20121205~ec7ac68f_armhf.deb
#RUN dpkg -i omxplayer_0.2.4~git20121205~ec7ac68f_armhf.deb
#Issue HERE
#RUN sudo apt-get install omxplayer

RUN /usr/bin/apt-get -y install fbset raspberrypi-sys-mods

RUN /usr/bin/apt-get -y install rng-tools

#RUN /usr/bin/apt-get -y install /tmp/cofi.deb

RUN /usr/bin/apt-get -y install raspi-config

RUN /usr/bin/apt-get -y install python-minimal python3-minimal python-dev python3-dev python-pip python3-pip python-setuptools python3-setuptools

RUN /usr/bin/apt-get -y install raspi-gpio python-rpi.gpio python3-rpi.gpio 
RUN /usr/bin/apt-get -y install python-gpiozero python3-gpiozero pigpio
RUN /usr/bin/apt-get -y install python-pigpio python3-pigpio python-serial
RUN /usr/bin/apt-get -y install python3-serial python-spidev python3-spidev
RUN /usr/bin/apt-get -y install python-smbus python3-smbus 
RUN /usr/bin/apt-get -y install python-astropi python3-astropi python-drumhat 
RUN /usr/bin/apt-get -y install python3-drumhat python-envirophat python3-envirophat 
RUN /usr/bin/apt-get -y install python-pianohat python3-pianohat python-pantilthat 
RUN /usr/bin/apt-get -y install python3-pantilthat python-scrollphat python3-scrollphat
RUN /usr/bin/apt-get -y install python-st7036 python3-st7036 python-sn3218 python3-sn3218
RUN /usr/bin/apt-get -y install python-piglow python3-piglow python-microdotphat 
RUN /usr/bin/apt-get -y install python3-microdotphat python-mote python3-mote python-motephat 
RUN /usr/bin/apt-get -y install python3-motephat python-explorerhat python3-explorerhat python-rainbowhat 
RUN /usr/bin/apt-get -y install python3-rainbowhat python-sense-hat python3-sense-hat 
RUN /usr/bin/apt-get -y install python-sense-emu python3-sense-emu sense-emu-tools 
RUN /usr/bin/apt-get -y install python-picamera python3-picamera python-rtimulib 
RUN /usr/bin/apt-get -y install python3-rtimulib python-pygame

RUN /usr/bin/apt-get -y install idle idle3

RUN /usr/bin/apt-get -y install ffmpeg rtmpdump

RUN /usr/bin/apt-get -y --no-install-recommends install ffmpeg youtube-dl

#RUN /usr/bin/apt-get -y install youtube-dlg

#issue here
#RUN sudo apt-get -y install wiringpi

RUN sudo apt-get -y install scratch

#RUN /usr/bin/apt-get -y install nuscratch

#RUN /usr/bin/apt-get -y install minecraft-pi python-picraft python3-picraft --allow-downgrades

#RUN /usr/bin/apt-get -y install sonic-pi

RUN apt-get update
RUN /usr/bin/apt-get -y -u dist-upgrade
RUN apt-get -u update
RUN /usr/bin/apt-get -y dist-upgrade

RUN /usr/bin/apt-get install -y --install-recommends xserver-xorg-core-hwe-16.04 xserver-xorg-input-all-hwe-16.04 xserver-xorg-input-evdev-hwe-16.04 xserver-xorg-input-synaptics-hwe-16.04 xserver-xorg-input-wacom-hwe-16.04 xserver-xorg-video-all-hwe-16.04 xserver-xorg-video-fbdev-hwe-16.04 xserver-xorg-video-vesa-hwe-16.04

#issue here
#RUN apt-daemon role='role-commit-packages' sender=':1.24'

RUN apt-get upgrade
RUN apt-get update
RUN sudo apt-get -y autoclean
RUN sudo apt-get -y autoremove 
RUN df
RUN apt-get -y install links2

#RUN apt-get -y install ros-kinetic-desktop

RUN apt install -y python-rosinstall python-rosinstall-generator python-wstool build-essential

#Drone development
#this one is to run the old range finder
RUN sudo apt-get install build-essential python-dev python-smbus git 

#this is for communincation with old range finder
RUN pip install smbus2
RUN pip install vl53l1x

#to get roscd, rosls
RUN bash /opt/ros/kinetic/setup.bash
RUN (cd /code/catkin_ws/src/ && catkin_create_pkg pidrone_pkg roscpp rospy geometry_msgs std_msgs message_generation std_msgs message_runtime)
ADD pidrone_pkg /code/catkin_ws/src/pidrone_pkg
RUN cd /code/catkin_ws && . /opt/ros/kinetic/setup.sh && catkin build --workspace ./
RUN apt install tree
CMD bash
SHELL ["/bin/bash"]

