import datetime

class BasicSensor:
    value = None
    name = None
    parameter = None
    type = "Basic"

    def __init__(self,name,parameter=None):
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
class CPUSensor(BasicSensor):
    type = "CPU_temp"
    def Refresh(self):
        try:
            cpu_sensor = open('/sys/class/thermal/thermal_zone0/temp')
            return int(cpu_sensor.read()) / 1000
        except:
            print('CPU temp sensor error', datetime.datetime.now())



DS18 = DS18Sensor("Sensor1","28-030197945ffe")
CPU = CPUSensor("CPU_temp")

print (DS18.value)
print(CPU.value)









