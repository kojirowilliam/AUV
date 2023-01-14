#!/bin/bash
NAME="my-gazebo-app"
docker image ls $NAME
echo "What do you want to tag this?"
read tag
docker build -t $NAME:$tag .
echo "Built $NAME:$tag"