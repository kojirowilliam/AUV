#!/bin/bash
NAME="my-gazebo-app"
tag="0"
docker image ls
echo "What do you want to tag this?"
docker build -t $NAME:$tag .
echo "Built $NAME:$tag"