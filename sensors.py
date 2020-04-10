import datetime
import os
import socket
import json
import time
from timeit import default_timer
import RPi.GPIO as GPIO
import dht11
from whatsminer import GetWhatsMinerInfo

class BasicDevice:
    Sensors =[]
    name = None
    type = "BasicDevice"

    def RefreshSensors(self):
        if len(self.Sensors)!= 0:
            for sensor in self.Sensors:
                sensor.Refresh()

class WhatsMiner(BasicDevice):
    ip = None
    port = None
    def __init__(self,name,ip,port):
        self.name = name
        self.ip = ip
        self.port = port
        response = GetWhatsMinerInfo(self.ip,self.port)
        self.Sensors.append()
        mhs = int(response['SUMMARY'][0]['MHS 5s'])
        freq = int(response['SUMMARY'][0]['freq_avg'])
        voltage = int(response['SUMMARY'][0]['Voltage'])
        power = int(response['SUMMARY'][0]['Power'])
        temperature = int(response['SUMMARY'][0]['Temperature'])
    def RefreshSensors(self):
        self.Sensors = []
        response = GetWhatsMinerInfo(self.ip, self.port)
        self.Sensors.append()
        self.Sensors.append(BasicSensor("MHS 5s",int(response['SUMMARY'][0]['MHS 5s'])))
        self.Sensors.append(BasicSensor("freq_avg", int(response['SUMMARY'][0]['freq_avg'])))
        self.Sensors.append(BasicSensor("Voltage", int(response['SUMMARY'][0]['Voltage'])))
        self.Sensors.append(BasicSensor("Power", int(response['SUMMARY'][0]['Power'])))
        self.Sensors.append(BasicSensor("Temperature", int(response['SUMMARY'][0]['Temperature'])))
        self.Sensors.append(BasicSensor("Fan Speed Out", int(response['SUMMARY'][0]['Fan Speed Out'])))
        self.Sensors.append(BasicSensor("Fan Speed In", int(response['SUMMARY'][0]['Fan Speed In'])))
        self.Sensors.append(BasicSensor("Power Fanspeed", int(response['SUMMARY'][0]['Power Fanspeed'])))


class BasicSensor:
    min = None
    max = None
    deviation = None

    value = None
    name = None
    parameter = None

    type = "BasicSensor"

    def __init__(self,name,parameter=None):
        self.name = name
        self.parameter = parameter
        self.value = self.Refresh()

    def GetValue(self):
        self.value = self.Refresh()
        return self.value

    def Refresh(self):
        return self.parameter

class DS18Sensor(BasicSensor):
    type = "DS18_temp"
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
class CPUTempSensor(BasicSensor):

    type = "CPU_temp"
    def Refresh(self):
        try:
            cpu_sensor = open('/sys/class/thermal/thermal_zone0/temp')
            return int(cpu_sensor.read()) / 1000
        except:
            print('CPU temp sensor error', datetime.datetime.now())

class HDDSpaceSensor(BasicSensor):
    type = "HDD_space"
    def Refresh(self):
        try:
            data = os.popen('df -h --output=source,pcent | grep root').read()
            return int(data.split(' ')[-1].replace('%', ''))
        except:
            print('Error GetHDDSpace()')

class TCPDelaySensor(BasicSensor):
    type = "TCP_Delay"
    def Refresh(self):

        try:

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            start = default_timer()
            s.connect((self.parameter, 443))
            end = default_timer()
            s.close()

            return round((end - start) * 1000, 1)
        except:

            return 0

class DHT11TemperatureSensor(BasicSensor):
    type = "DHT11_humidity"
    instance = None
    def __init__(self,name,parameter):
        self.name = name
        self.parameter = parameter
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.cleanup()
        self.instance = dht11.DHT11(pin=parameter)
        self.value = self.Refresh()

    def Refresh(self):
        try:
            for x in range(0, 10):
                result = self.instance.read()
                if result.is_valid() and result.temperature != 0:
                    return result.temperature
                    break
                time.sleep(1)
            return -127
        except:
            print('DHT11 read error')
            return -127


#DS18 = DS18Sensor("Sensor1","28-030197945ffe")
#CPU = CPUTempSensor("CPU1_temp")
#HDD = HDDSpaceSensor("HDD1_space")
#Internet = TCPDelaySensor("google delay","google.com")
#DHT11= DHT11TemperatureSensor("DHT_temp",26)
miner1 = WhatsMiner("miner1",'192.168.10.10','4028')
for s in miner1.Sensors:
    print(s.name,s.value)


#print (DS18.value)
#print(CPU.value)
#print(HDD.value)
#print(Internet.value)
#print(DHT11.value)









