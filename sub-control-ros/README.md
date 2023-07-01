# AUV ROS Control Architecture

Written in Python, this code includes a editable framework for the implementation of multiple types of controllers that can be toggled through the use of a finite state machine. 

## fsm_basic

Used for testing. Contains code that allows keyboard interaction when run in Python shell. Keys 1-8 control thrusters 1-8 individually with a constant positive thrust value.

## fsm_pcontrol

Controls mantaray using PID feedback control. 6 DOF allows translation in *x*, *y*, and *z* direction, and roll, pitch, and yaw. Currently under development.

## Quaternion PID Controller Architecture

The control architecture was implemented by me based on the article below, using the schematic as a reference guide. 

---
![Controller Architecture](/sub-control-ros/quaternion_controller_architecture.png)

---

Gołąbek, M.; Welcer, M.; Szczepański, C.; Krawczyk, M.; Zajdel, A.; Borodacz, K. Quaternion Attitude Control System of Highly Maneuverable Aircraft. Electronics 2022, 11, 3775. https://doi.org/10.3390/electronics11223775


