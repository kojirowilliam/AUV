I initially planned to implement the Zed-M camera using the zed-ros-wrapper, but it was more difficult that I initially
anticipated it would be because the ROS package was made for Noetic and above all, the zed-ros-wrapper was not made
to work with Gazebo. It seems like it requires the hardware as well for it to work properly. So for the sake of saving
time, I decided to create my own camera sensor from scratch that best mimics what we would get from the Zed-M camera.

Basically everything is based off of the zed-ros-wrapper since a lot of the code from the repo has useful information
that I can use to create my own Depth Camera.


Author: William Y.