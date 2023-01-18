FROM ros:melodic

# install basic ubuntu tools
# RUN apt-get 

# install uuv_simulator package
RUN apt-get update && apt install -y ros-melodic-uuv-simulator

RUN echo 'Etc/UTC' > /etc/timezone && \
    rm -r /etc/localtime && \
    ln -s /usr/share/zoneinfo/Etc/UTC /etc/localtime && \
    apt-get update && \
    apt-get install -q -y --no-install-recommends tzdata && \
    rm -rf /var/lib/apt/lists/*

# RUN apt-get update && apt-get install -y lsb-release wget gnupg apt-utils && \
#     wget https://packages.osrfoundation.org/gazebo.gpg -O /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg && \
#     echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] \
#     http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | \
#     tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null && \
#     apt-get update && \
#     apt-get install -y gz-garden && \
#     rm -rf /var/lib/apt/lists/*

EXPOSE 11345

RUN ls

# ENTRYPOINT ["/gzserver_entrypoint.sh"]

# launch ros package
# RUN roslaunch uuv_gazebo_worlds auv_underwater_world.launch
# CMD ["roslaunch", "uuv_gazebo_worlds", "auv_underwater_world.launch"]