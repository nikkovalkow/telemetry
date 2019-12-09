import RPi.GPIO as GPIO
from pymongo import MongoClient
import time
import datetime

def GetTemperature():
    try:
        device = open('/sys/bus/w1/devices/28-030c97940c83/w1_slave','r')
        output = device.read()
        if output.find('YES')!=-1:
            return int(output[output.find('t=')+2:])/1000
        else:
            print('Temp sensor crc error',datetime.datetime.now())
            
    except:
        print('Temp sensor error',datetime.datetime.now())

def GetCPUTemp():
    try:
        cpu_sensor= open('/sys/class/thermal/thermal_zone0/temp')
        return int(cpu_sensor.read())/1000
    except:
        print('CPU temp sensor error',datetime.datetime.now())

client = MongoClient('localhost',27017)

db = client['sensors']
col= db['temperature']

while 1:
    
    testdata={ 'time':datetime.datetime.now(),'sensor':1,'temp' : GetTemperature() }
    col.insert_one(testdata)

    testdata={ 'time':datetime.datetime.now(),'sensor':0,'temp' : GetCPUTemp() }
    col.insert_one(testdata)

    time.sleep(30)

client.close()
