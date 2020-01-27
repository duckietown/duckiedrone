# parameters
ARG REPO_NAME="cleandrone"

# ==================================================>
# ==> Do not change this code
ARG ARCH=arm32v7
ARG MAJOR=daffy
ARG BASE_TAG=${MAJOR}-${ARCH}
ARG BASE_IMAGE=dt-ros-commons

# define base image
FROM duckietown/${BASE_IMAGE}:${BASE_TAG}

# define repository path
ARG REPO_NAME
ARG REPO_PATH="${CATKIN_WS_DIR}/src/${REPO_NAME}"

# create repo directory
RUN mkdir -p "${REPO_PATH}"
WORKDIR "${REPO_PATH}"



# TODO
ENV DEBIAN_FRONTEND=noninteractive
RUN rm -rf /etc/apt/*
ADD assets/apt_from_drone /etc/apt/

# raspberry pi stuff
RUN apt-get update \
  && apt-get install \
    --yes \
    --no-install-recommends \
    --option Dpkg::Options::="--force-confdef" \
    --option Dpkg::Options::="--force-confold" \
        libraspberrypi0 \
        libraspberrypi-bin \
        libraspberrypi-dev \
        libraspberrypi-doc \
        raspberrypi-bootloader \
  && rm -rf /var/lib/apt/lists/*

# TODO



# install apt dependencies
COPY ./dependencies-apt.txt "${REPO_PATH}/"
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    $(awk -F: '/^[^#]/ { print $1 }' dependencies-apt.txt | uniq) \
  && rm -rf /var/lib/apt/lists/*




# install python dependencies
COPY ./dependencies-py3.txt "${REPO_PATH}/"
RUN pip install -r ${REPO_PATH}/dependencies-py3.txt

# copy the source code
COPY . "${REPO_PATH}/"

# build packages
RUN . /opt/ros/${ROS_DISTRO}/setup.sh && \
  catkin build \
    --workspace ${CATKIN_WS_DIR}/

# define launch script
ENV LAUNCHFILE "${REPO_PATH}/launch.sh"

# define command
CMD ["bash", "-c", "${LAUNCHFILE}"]

# store module name
LABEL org.duckietown.label.module.type="${REPO_NAME}"
ENV DT_MODULE_TYPE "${REPO_NAME}"

# store module metadata
ARG ARCH
ARG MAJOR
ARG BASE_TAG
ARG BASE_IMAGE
LABEL org.duckietown.label.architecture="${ARCH}"
LABEL org.duckietown.label.code.location="${REPO_PATH}"
LABEL org.duckietown.label.code.version.major="${MAJOR}"
LABEL org.duckietown.label.base.image="${BASE_IMAGE}:${BASE_TAG}"
# <== Do not change this code
# <==================================================

MAINTAINER Arthur MacKeith <amackeith@uchicago.edu>










#ARG ARCH=arm32v7
#FROM duckietown/dt-ros-commons:daffy-${ARCH}
#
#


RUN apt-get update

#RUN apt-get --yes --force-yes -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" install libraspberrypi0
#RUN apt-get --yes --force-yes -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" install libraspberrypi-bin
#RUN apt-get --yes --force-yes -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" install libraspberrypi-dev
#RUN apt-get --yes --force-yes -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" install libraspberrypi-doc
#RUN apt-get --yes --force-yes -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" install raspberrypi-bootloader


RUN apt-get --yes upgrade bluez-firmware linux-firmware pi-bluetooth
RUN apt-get -y upgrade hostapd --fix-missing



##RUN sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
##RUN apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net:80 --recv-key 421C365BD9FF1F717815A3895523BAEEB01FA116






#RUN apt-get -y install --install-recommends xserver-xorg-core-hwe-16.04 xserver-xorg-input-all-hwe-16.04 xserver-xorg-input-evdev-hwe-16.04 xserver-xorg-input-synaptics-hwe-16.04 xserver-xorg-input-wacom-hwe-16.04 xserver-xorg-video-all-hwe-16.04 xserver-xorg-video-fbdev-hwe-16.04 xserver-xorg-video-vesa-hwe-16.04
#RUN apt-get -y install xserver-xorg-video-fbturbo



RUN apt-get -y upgrade
RUN apt-get -y dist-upgrade
RUN apt-get -y autoclean
RUN apt-get -y autoremove


SHELL ["/bin/bash"]

