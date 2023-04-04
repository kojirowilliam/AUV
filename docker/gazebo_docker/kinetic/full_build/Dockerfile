FROM gazebo_auv:kinetic_updated

RUN apt-get update && apt-get install -y \
      python-catkin-tools \
    && rm -rf /var/lib/apt/lists/*

# clone ros package repo
ENV CATKIN_WS /opt/catkin_ws
WORKDIR $CATKIN_WS

RUN cd ~/catkin_ws && catkin_make

RUN roslaunch rexrov2_gazebo start_demo_pid_controller.launch teleop_on:=true joy_id:=0
CMD ["roslaunch", "uuv_gazebo_worlds", "auv_underwater_world.launch"]