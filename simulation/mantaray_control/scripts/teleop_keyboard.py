#!/usr/bin/env python

from __future__ import print_function

import threading

# import roslib; roslib.load_manifest('teleop_keyboard')
import rospy

from uuv_gazebo_ros_plugins_msgs.msg import FloatStamped
from thruster import Thruster

import sys
from select import select

if sys.platform == 'win32':
    import msvcrt
else:
    import termios
    import tty


msg = """
Reading from the keyboard  and Publishing to FloatStamped!
REQUIRES you to type in the terminal!
---------------------------
Moving each thruster from 1-8 and q-i

Change speed by holding down the shift key:

Press 0 to stop moving

CTRL-C to quit
"""

# moveBindings = {
#         '1':(1,0,0,0,0,0,0,0),
#         '2':(0,1,0,0,0,0,0,0),
#         '3':(0,0,1,0,0,0,0,0),
#         '4':(0,0,0,1,0,0,0,0),
#         '5':(0,0,0,0,1,0,0,0),
#         '6':(0,0,0,0,0,1,0,0),
#         '7':(0,0,0,0,0,0,1,0),
#         '8':(0,0,0,0,0,0,0,1),
#         'i':(1,0,0,0),
#         'o':(1,0,0,-1),
#         'j':(0,0,0,1),
#         'l':(0,0,0,-1),
#         'u':(1,0,0,1),
#         ',':(-1,0,0,0),
#         '.':(-1,0,0,1),
#         'm':(-1,0,0,-1),
#         'O':(1,-1,0,0),
#         'I':(1,0,0,0),
#         'J':(0,1,0,0),
#         'L':(0,-1,0,0),
#         'U':(1,1,0,0),
#         '<':(-1,0,0,0),
#         '>':(-1,-1,0,0),
#         'M':(-1,1,0,0),
#         't':(0,0,1,0),
#         'b':(0,0,-1,0),
#     }

moveBindings = {
        '1':(1,0,0,0,0,0,0,0),
        '2':(0,1,0,0,0,0,0,0),
        '3':(0,0,1,0,0,0,0,0),
        '4':(0,0,0,1,0,0,0,0),
        '5':(0,0,0,0,1,0,0,0),
        '6':(0,0,0,0,0,1,0,0),
        '7':(0,0,0,0,0,0,1,0),
        '8':(0,0,0,0,0,0,0,1),
        '0':(None,None,None,None,None,None,None,None),
        'q':(-1,0,0,0,0,0,0,0),
        'w':(0,-1,0,0,0,0,0,0),
        'e':(0,0,-1,0,0,0,0,0),
        'r':(0,0,0,-1,0,0,0,0),
        't':(0,0,0,0,-1,0,0,0),
        'y':(0,0,0,0,0,-1,0,0),
        'u':(0,0,0,0,0,0,-1,0),
        'i':(0,0,0,0,0,0,0,-1)
    }

speedBindings={
        '!':(1,0,0,0,0,0,0,0),
        '@':(0,1,0,0,0,0,0,0),
        '#':(0,0,1,0,0,0,0,0),
        '$':(0,0,0,1,0,0,0,0),
        '%':(0,0,0,0,1,0,0,0),
        '^':(0,0,0,0,0,1,0,0),
        '&':(0,0,0,0,0,0,1,0),
        '*':(0,0,0,0,0,0,0,1),
        'Q':(-1,0,0,0,0,0,0,0),
        'W':(0,-1,0,0,0,0,0,0),
        'E':(0,0,-1,0,0,0,0,0),
        'R':(0,0,0,-1,0,0,0,0),
        'T':(0,0,0,0,-1,0,0,0),
        'Y':(0,0,0,0,0,-1,0,0),
        'U':(0,0,0,0,0,0,-1,0),
        'I':(0,0,0,0,0,0,0,-1)
    }

class PublishThread(threading.Thread):
    def __init__(self, rate, namespace, thruster_count):
        super(PublishThread, self).__init__()
        self.namespace = namespace
        self.thruster_count = thruster_count
        self.publishers = [rospy.Publisher('/' + namespace + '/thrusters/'+str(i)+'/input', FloatStamped, queue_size = 10) for i in range(self.thruster_count)]
        self.thrusters_data = [0] * self.thruster_count
        self.condition = threading.Condition()
        self.done = False

        # Set timeout to None if rate is 0 (causes new_message to wait forever
        # for new data to publish)
        if rate != 0.0:
            self.timeout = 1.0 / rate
        else:
            self.timeout = None

        self.start()

    def wait_for_subscribers(self):
        for publisher in self.publishers:
            i = 0
            while not rospy.is_shutdown() and publisher.get_num_connections() == 0:
                if i == 4:
                    print("Waiting for subscriber to connect to {}".format(publisher.name))
                rospy.sleep(0.5)
                i += 1
                i = i % 5
            if rospy.is_shutdown():
                raise Exception("Got shutdown request before subscribers connected")

    def update(self, thrusters):
        self.condition.acquire()
        self.thrusters_data = thrusters
        # Notify publish thread that we have a new message.
        self.condition.notify()
        self.condition.release()

    def stop(self):
        self.done = True
        self.update([0]*8)
        self.join()

    def run(self):
        float_msgs = [FloatStamped() for i in range(self.thruster_count)]
        for i in range(self.thruster_count):
            float_msgs[i].header.frame_id = float_frame
        while not self.done:
            for i in range(self.thruster_count):
                float_msgs[i].header.stamp = rospy.Time.now()
            self.condition.acquire()
            # Wait for a new message or timeout.
            self.condition.wait(self.timeout)

            # Copy state into twist message.
            print("Printing thruster outs")
            for i in range(self.thruster_count):
                print(self.thrusters_data[i])
                float_msgs[i].data = self.thrusters_data[i]
                print(float_msgs[i])
            self.condition.release()

            # Publish.
            for i in range(self.thruster_count):
                self.publishers[i].publish(float_msgs[i])

        # Publish stop message when thread exits.
        for i in range(self.thruster_count):
            float_msgs[i].data = 0
            self.publishers[i].publish(float_msgs[i])


def getKey(settings, timeout):
    if sys.platform == 'win32':
        # getwch() returns a string on Windows
        key = msvcrt.getwch()
    else:
        tty.setraw(sys.stdin.fileno())
        # sys.stdin.read() returns a string on Linux
        rlist, _, _ = select([sys.stdin], [], [], timeout)
        if rlist:
            key = sys.stdin.read(1)
        else:
            key = ''
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def saveTerminalSettings():
    if sys.platform == 'win32':
        return None
    return termios.tcgetattr(sys.stdin)

def restoreTerminalSettings(old_settings):
    if sys.platform == 'win32':
        return
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

def vels(speed, turn):
    return "currently:\tspeed %s\tturn %s " % (speed,turn)

if __name__=="__main__":
    settings = saveTerminalSettings()

    rospy.init_node('teleop_twist_keyboard')

    namespace = rospy.get_param("~ns", 'mantaray')
    thruster_count = rospy.get_param("thruster_count", 8)
    speed = rospy.get_param("~speed", 0.1)
    simple_thrust = rospy.get_param("~simple_thrust", 0.5)
    saturation = rospy.get_param("~speed_limit", 2)
    repeat = rospy.get_param("~repeat_rate", 0.0)
    key_timeout = rospy.get_param("~key_timeout", 0.5)
    float_frame = rospy.get_param("~frame_id", '')

    pub_thread = PublishThread(repeat, namespace, thruster_count)

    thrusters = [Thruster(saturation) for i in range(thruster_count)]
    x = 0
    y = 0
    z = 0
    th = 0
    status = 0

    try:
        pub_thread.wait_for_subscribers()
        pub_thread.update([thruster.get_thrust() for thruster in thrusters])

        print(msg)
        # print(vels(speed,turn))
        while(1):
            key = getKey(settings, key_timeout)

            if key in moveBindings.keys():
                for i in range(thruster_count):
                    if (moveBindings[key][i] == None):
                        thrusters[i].reset()
                    elif (moveBindings[key][i] != 0):
                        thrusters[i].set_thrust(moveBindings[key][i] * simple_thrust)
            elif key in speedBindings.keys():
                for i in range(thruster_count):
                    if speedBindings[key][i]:
                        thrusters[i].add_thrust(speedBindings[key][i] * speed)
            else:
                # Skip updating cmd_vel if key timeout and robot already
                # stopped.
                if key == '' and x == 0 and y == 0 and z == 0 and th == 0:
                    continue
                x = 0
                y = 0
                z = 0
                th = 0
                if (key == '\x03'):
                    break

            pub_thread.update([thruster.get_thrust() for thruster in thrusters])

    except Exception as e:
        print(e)

    finally:
        pub_thread.stop()
        restoreTerminalSettings(settings)