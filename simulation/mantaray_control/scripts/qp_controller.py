'''
A Quaternion-Based PID controller (Or at least my shitty attempt at making one)

Description:
Quaternions are hard to visualize, but if you think of the three scalars as points
that dictate the axis of rotation where their magnitudes are how much they influence
the axis of rotation, it isn't that hard. The scalar is then just how much the object
rotates around the axis of rotation created by the three scalars.

Plan:
I plan on creating a P controller first that tries to control the roll of the sub. This
requires using the 
Then I'll create one that controls the pitch of the sub.
Finally, I'll create one that controls the yaw of the sub.
'''