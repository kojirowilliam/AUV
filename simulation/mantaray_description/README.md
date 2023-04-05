
---
<h1>Instructions</h1>
<br>
<ol>
<li>To be able to modify this file without keeping it out of sync with the repo, you should create a symbolic link to this file inside of your catkin workspace. This can be done by running a command similar to this from inside the src/ folder of your catkin workspace
    
    ln -s ~/AUV/simulation/mantaray_description mantaray_description
    
where <code>~/AUV/simulation/mantaray_description</code> is this mantaray_description/ folder and mantaray_description is simply the name of the linked folder that will be created inside of the src/ folder of your catkin workspace.
</li>



<li>Run <code>catkin_make</code> in ~/catkin_ws</li>
</ol>
<br>

---
<h2>Tests:</h2>
<h3>Test to see if mantaray_description was built properly</h3>
<ol>
<li>Run an empty ocean environment:</li>
    
    roslaunch uuv_gazebo_worlds empty_underwater_world.launch

<li>Next upload the mantaray sub into the empty ocean environment:</li>

    roslaunch mantaray_description upload.launch 

</ol>
<br>
<h3>Test to see if thruster 0 works</h3>
<ol>
<li>Get the sub in a gazebo world (Continue from the above test)</li>
<li>On a separate terminal, run the following:</li>
    
    rostopic pub -1 /mantaray/thrusters/0/input uuv_gazebo_ros_plugins_msgs/FloatStamped -- '
    {
    header: {seq: 13000, stamp: now},
    data: 100
    }'

</ol>
---
<h2>Contacts</h2>
<p2>If things don't work, let me know through Slack <strong>@William Yamada</strong></p2>
