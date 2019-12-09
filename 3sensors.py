import RPi.GPIO as GPIO
from pymongo import MongoClient
import time
import datetime

sensors=['28-030197945ffe','28-03029794645a', '28-030c97940c83']

def GetTemperatureDS18(sensor):
    try:
        device = open('/sys/bus/w1/devices/'+sensor+'/w1_slave','r')
        output = device.read()
        if output.find('YES')!=-1:
            return int(output[output.find('t=')+2:])/1000
        else:
            print('Temp sensor crc error',datetime.datetime.now())
            
    except:
        
        print('Temp sensor error',datetime.datetime.now())


while 1:
    
    for s in sensors: 
        print(s,GetTemperature(s))
    print('--------------------')
    time.sleep(3)
        
