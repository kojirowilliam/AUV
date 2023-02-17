#!/usr/bin/env bash
NUM_ARGS=$#
X=$1
Y=$2
Z=$3

# echo There are $NUM_ARGS arguments which are $X, $Y, $Z
if [[$NUM_ARGS -eq 3]]; then
    rosservice call /rexrov2/go_to "
{
waypoint: {
header: {seq: 0, stamp: now},
point: {x: $X, y: $Y, z: $Z},
max_forward_speed: 10.0,
heading_offset: 0.0,
use_fixed_heading: false,
radius_of_acceptance: 1.0},
max_forward_speed: 1.0,
interpolator: LINEAR
}"
else
    rosservice call /rexrov2/go_to '
{
waypoint: {
header: {seq: 0, stamp: now},
point: {x: 20.0, y: 10.0, z: -100.0},
max_forward_speed: 10.0,
heading_offset: 0.0,
use_fixed_heading: false,
radius_of_acceptance: 1.0},
max_forward_speed: 1.0,
interpolator: LINEAR
}'
fi