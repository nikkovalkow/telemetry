import datetime

class BasicSensor:
    value = None
    name = None
    parameter = None
    type = "Basic"

    def __init__(self,name,parameter):
        self.name = name
        self.parameter = parameter
        self.value = self.Refresh()

    def GetValue(self):
        return self.value

    def Refresh(self):
        return 100

class DHTSensor(BasicSensor):
    type = "DHT"
    def Refresh(self):
        return 200

class DS18Sensor(BasicSensor):
    type = "DS18"
    def Refresh(self):
        try:
            device = open('/sys/bus/w1/devices/' + self.parameter + '/w1_slave', 'r')
            output = device.read()
            if output.find('YES') != -1:
                return int(output[output.find('t=') + 2:]) / 1000
            else:
                print('Temp sensor crc error', datetime.datetime.now())

        except:

            print('Temp sensor error', datetime.datetime.now())


DS18 = DS18Sensor("Sensor1","28-030197945ffe")

print (DS18.value)









