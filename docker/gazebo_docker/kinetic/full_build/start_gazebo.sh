#!/bin/bash
IMAGE_NAME="gazebo_auv"
CONTAINER_NAME="gazebo-auv-app"
docker image ls $IMAGE_NAME
echo "What version of $IMAGE_NAME would you like to use?"
read tag
xhost +local:root
docker_version=0

sudo docker run --gpus all -e NVIDIA_DRIVER_CAPABILITIES=all \
--privileged -e DISPLAY=$DISPLAY -it \
-v /tmp/.X11-unix/:/tmp/.X11-unix/ \
-v="/tmp/.gazebo/:/root/.gazebo/" \
--name $CONTAINER_NAME $IMAGE_NAME:$tag
