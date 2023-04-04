FROM ros:kinetic

# install basic ubuntu tools
# RUN apt-get 

# install uuv_simulator package
RUN apt-get update && apt install -y ros-kinetic-uuv-simulator && \
    echo "source /opt/ros/kinetic/setup.bash" >> ~/.bashrc

# RUN sudo sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list' wget https://packages.osrfoundation.org/gazebo.key -O - | sudo apt-key add - && \
#     sudo apt-get update && \
#     sudo apt-get install -y gazebo9 && \
#     sudo apt-get install -y libgazebo9-dev

RUN echo 'Etc/UTC' > /etc/timezone && \
    rm -r /etc/localtime && \
    ln -s /usr/share/zoneinfo/Etc/UTC /etc/localtime && \
    apt-get update && \
    apt-get install -q -y --no-install-recommends tzdata && \
    apt-get install -y vim && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p ~/catkin_ws/src && cd ~/catkin_ws/src && \
    git clone https://github.com/uuvsimulator/rexrov2.git && \
    git clone https://github.com/uuvsimulator/uuv_simulation_evaluation.git && \
    cd ~/catkin_ws/src/uuv_simulation_evaluation/uuv_smac_utils && \
    sed -i '14 i \ \ <build_depend>uuv_simulation_evaluation</build_depend>' package.xml

# RUN /bin/bash -c "source ~/.bashrc"
# RUN --mount=type=cache,target=~/.bashrc
# RUN cd ~/catkin_ws

RUN /bin/bash -c '. /opt/ros/kinetic/setup.bash; cd ~/catkin_ws; catkin_make'

# RUN cd ~/catkin_ws && catkin_make
    # use sed not echo
RUN  echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc && . ~/.bashrc 

RUN apt-get update && apt-get install -y lsb-release wget gnupg apt-utils && \
    wget https://packages.osrfoundation.org/gazebo.gpg -O /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] \
    http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | \
    tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null && \
    apt-get update && \
    apt-get install -y gz-garden && \
    rm -rf /var/lib/apt/lists/*

EXPOSE 11345

# RUN ls

# ENTRYPOINT ["/gzserver_entrypoint.sh"]

# launch ros package
# RUN roslaunch uuv_gazebo_worlds auv_underwater_world.launch
# RUN roslaunch rexrov2_gazebo start_demo_pid_controller.launch teleop_on:=true joy_id:=0
# CMD ["roslaunch", "uuv_gazebo_worlds", "auv_underwater_world.launch"]