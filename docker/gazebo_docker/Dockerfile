FROM ros:melodic

# install basic ubuntu tools
# RUN apt-get 

# install uuv_simulator package


RUN apt-get update && apt install -y ros-melodic-uuv-simulator

# RUN sudo sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list' wget https://packages.osrfoundation.org/gazebo.key -O - | sudo apt-key add - && \
#     sudo apt-get update && \
#     sudo apt-get install -y gazebo9 && \
#     sudo apt-get install -y libgazebo9-dev

RUN echo 'Etc/UTC' > /etc/timezone && \
    rm -r /etc/localtime && \
    ln -s /usr/share/zoneinfo/Etc/UTC /etc/localtime && \
    apt-get update && \
    apt-get install -q -y --no-install-recommends tzdata && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir ~/catkin_ws && cd ~/catkin_ws && mkdir src && cd src && \
    git clone https://github.com/uuvsimulator/rexrov2.git 
    # git clone https://github.com/uuvsimulator/uuv_simulation_evaluation.git
    
    
    # source devel/setup.bash 
    # && source ~/.bashrc && catkin_make && source devel/setup.bash
# RUN cd ~/catkin_ws && catkin_make && \
#     cd uuv_simulation_evaluation/uuv_simulation_wrapper && cmake .

# RUN source devel/setup.bash


# RUN apt-get update && apt-get install -y lsb-release wget gnupg apt-utils && \
#     wget https://packages.osrfoundation.org/gazebo.gpg -O /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg && \
#     echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] \
#     http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | \
#     tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null && \
#     apt-get update && \
#     apt-get install -y gz-garden && \
#     rm -rf /var/lib/apt/lists/*

EXPOSE 11345

# RUN ls

# ENTRYPOINT ["/gzserver_entrypoint.sh"]

# launch ros package
# RUN roslaunch uuv_gazebo_worlds auv_underwater_world.launch
# RUN roslaunch rexrov2_gazebo start_demo_pid_controller.launch teleop_on:=true joy_id:=0
# CMD ["roslaunch", "uuv_gazebo_worlds", "auv_underwater_world.launch"]