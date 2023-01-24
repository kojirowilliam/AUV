import rospy
from beginner_tutorials.msg import Sensor

import struct
import math
import serial

def decode(data):
    messages = []
    return _process_packet(data, -1, messages)


def _process_packet(data, timestamp, messages):
    if data == b'':
        pass
    elif data[0] == 35:  # if packet is a bundle ("#" = ASCII 35)
        timetag, contents = _process_bundle(data)
        timestamp = timetag / pow(2, 32)  # convert to seconds since January 1, 1900. See https://en.wikipedia.org/wiki/Network_Time_Protocol#Timestamps
        for content in contents:
            _process_packet(content, timestamp, messages)  # call recursively
    elif data[0] == 47:  # if packet is a message ("#" = ASCII 47)
        message = _process_message(data)
        if timestamp != -1:
            message[0] = timestamp
        messages.append(message)
    return messages


def _process_bundle(data):
    #NOTE: There seems to be an extra byte from the timetag sometimes.
    offset = 0
    if (data[15:16] != b'\x00'):
        offset += 1
    timetag = int.from_bytes(data[8:(16+offset)], byteorder='big')  # timetag is uint64 starting at index 8
    elements = data[(16+offset):]  # all remaining bytes are contiguous bundle elements
    contents = []
    while len(elements) > 0:
        size = int.from_bytes(elements[0:4], byteorder='big')  # element size is uint32 starting at index 0
        contents.append(elements[4: (size + 4)])  # follow size number of bytes are OSC contents
        elements = elements[(size + 4):]  # skip to next element
    return timetag, contents


def _process_message(data):
    message = [-1, data[0:data.index(0)].decode("utf-8")]  # timestamp = -1, get address as string up to "\0"
    remaining = data[data.index(44):]  # type tags and arguments start at ","
    type_tags = remaining[0:(remaining.index(0) + 1)].decode("utf-8")  # type tags end at "\0"
    arguments = remaining[(4 * math.ceil(len(type_tags) / 4)):]  # account for trailing "\0" characters
    for type_tag in type_tags:
        if type_tag == ",":  # first character of type tag string
            continue
        elif type_tag == "i":  # argument is uint32
            message.append(int.from_bytes(arguments[0:4], byteorder='big'))
            arguments = arguments[4:]
        elif type_tag == "f":  # argument is float
            float_bytes = bytearray(arguments[0:4])
            float_bytes.reverse()
            message.append(struct.unpack('f', float_bytes)[0])
            arguments = arguments[4:]
        elif type_tag == "\x00":  # last character of type tag string
            continue
        elif type_tag == "s" or type_tag == "S":  # argument is string
            message.append(arguments[0:arguments.index(0)].decode("utf-8"))
            arguments = arguments[(4 * math.ceil((len(message[-1]) + 1) / 4)):]  # account for trailing "\0" characters
        elif type_tag == "b":  # argument is blob
            size = int.from_bytes(arguments[0:4], byteorder='big')
            message.append(arguments[4:(4 + size)])
            arguments = arguments[4 + (4 * math.ceil(size / 4)):]  # account for trailing "\0" characters
        elif type_tag == "T":  # argument is True
            message.append(True)
        elif type_tag == "F":  # argument is False
            message.append(False)
        else:
            print("Argument type not supported.", type_tag)
            break
    return message


class MySerial(serial.Serial):
    def _readline(self):
        eol = b'\xc0'
        leneol = len(eol)
        line = bytearray()
        while True:
            c = self.read(1)
            if c:
                line += c
                if line[-leneol:] == eol:
                    break
            else:
                break
        return bytes(line)

def talker():
    pub = rospy.Publisher('sensorChatter', Sensor, queue_size=10)
    rospy.init_node('sensorTalker', anonymous=True)
    rate = rospy.Rate(10) # 10hz

    serialObj = MySerial('/dev/ttyACM0', 115200, bytesize=8, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                        rtscts=1)
    
    while not rospy.is_shutdown():
        data = serialObj._readline()
        data = decode(data)
        sensorData = Sensor()
        # rospy.loginfo(data)
        if (data != [] and data[0][1] == "/sensors"):
            sensorData.xGyro = data[0][2]
            sensorData.yGyro = data[0][3]
            sensorData.zGyro = data[0][4]
            sensorData.xAccel = data[0][5]
            sensorData.yAccel = data[0][6]
            sensorData.zAccel = data[0][7]
            sensorData.xMagnet = data[0][8]
            sensorData.yMagnet = data[0][9]
            sensorData.zMagnet = data[0][10]
            sensorData.baro = data[0][11]
            rospy.loginfo(sensorData)
            pub.publish(sensorData)
            rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
