import time
import osc_decoder
import serial

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

class sensor(): # The parent class for all sensors
    def __init__(self, sensorName, sensorType, cacheSize = 200):
        self.name = sensorName
        self.type = sensorType
        self.cacheSize = cacheSize
        self.cache = []
        self.currentValue = []

    def getData(self):
        return self.currentValue

    def setData(self, data, setCache=True):
        # Sets the current value
        # if <setCache> is true, records previous data into <self.cache>
        if setCache:
            self.updateCache(data)
        self.currentValue = data

    def updateCache(self, data):
        self.cache.append(data)
        if len(self.cache) >= self.cacheSize:
            self.cache.pop(0)

class gyroscopeSensor(sensor):
    #TODO:LANCE Create docstrings for this function
    def __init__(self, sensorName, cacheSize=200):
        sensor.__init__(self, sensorName, "gyro", cacheSize)
    # returns acceleration x, y, z in g's
    def getVelocity(self):
        for l in self.currentValue:
            if l[1] == "/sensors":
                return [l[2],l[3],l[4]]
    
class accelerometerSensor(sensor):
    #TODO:LANCE Create docstrings for this function
    def __init__(self, sensorName, cacheSize=200):
        sensor.__init__(self, sensorName, "accel", cacheSize)
    # returns acceleration x, y, z in g's
    def getAcceleration(self):
        for l in self.currentValue:
            if l[1] == "/sensors":
                return [l[5],l[6],l[7]]

class barometerSensor(sensor):
    #TODO:LANCE Create docstrings for this function
    def __init__(self, sensorName, cacheSize=200):
        sensor.__init__(self, sensorName, "baro", cacheSize)
    # returns acceleration x, y, z in g's
    def getPressure(self):
        for l in self.currentValue:
            if l[1] == "/sensors":
                return l[11]
            
class magnetometerSensor(sensor):
    #TODO:LANCE Create docstrings for this function
    def __init__(self, sensorName, cacheSize=200):
        sensor.__init__(self, sensorName, "mag", cacheSize)
    # returns acceleration x, y, z in g's
    def getField(self):
        for l in self.currentValue:
            if l[1] == "/sensors":
                return [l[8],l[9],l[10]]
            
# gyroscope - angular velocity x, y, z (2,3,4)
# accelerometer - acceleration (g) x, y, z (5,6,7)
# magnetometer - micro teslas x, y, z (8,9,10)
# barometer - hPa (11) 


serialObj = MySerial('/dev/ttyACM0', 115200, bytesize=8, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                          rtscts=1)
cache = []

g = gyroscopeSensor("gyro1")
a = accelerometerSensor("accel1")
m = magnetometerSensor("maga")
b = barometerSensor("barista")


for i in range(10000):
    data = serialObj._readline()

    # if data == b'\xc0': #b'\xf3'
    try:
        data = osc_decoder.decode(data)
        g.setData(data)
        a.setData(data)
        m.setData(data)
        b.setData(data)
        
        accel = a.getAcceleration()
        velo = g.getVelocity()
        field = m.getField()
        pres = b.getPressure()
        if accel != None:
            print (f"accel: {accel}")
        if velo != None:
            print (f"rot velo: {velo}")
        if field != None:
            print (f"mag f: {field}")
        if pres != None:
            print (f"pres: {pres}")
    except:
        raise RuntimeError(f"Failed to get {data}")

serialObj.close()