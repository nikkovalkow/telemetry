import RPi.GPIO as GPIO
from pymongo import MongoClient
import time
import datetime
from sendsms import SendSMS

import RPi.GPIO as GPIO
import dht11

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
instance = dht11.DHT11(pin = 26)
SmsIsSent=False

sensors=['28-030197945ffe','28-03029794645a', '28-030c97940c83']

def GetHumidity():
    
    
    for x in range(0,20):
        result = instance.read()
        if result.is_valid():
            return result.humidity
            break
        
    
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

client = MongoClient('localhost',27017)

db = client['sensors']
col= db['temperature']

while 1:
    testdata={ 'time':datetime.datetime.now(),'sensor':0,'temp' : GetCPUTemp() }
    col.insert_one(testdata)
    sensor_number=1

    for s in sensors:
        testdata={ 'time':datetime.datetime.now(),'sensor':sensor_number,'temp' : GetTemperatureDS18(s) }
        col.insert_one(testdata)
        sensor_number = sensor_number + 1
        print(int(testdata['temp']))
        if (int(testdata['temp']) > 73) and not SmsIsSent:
            SendSMS('Sensor '+str(sensor_number)+' temperature '+str(testdata['temp']))
            #SendSMS('Hello world11')
            print ("Temperature warning!")
            SmsIsSent=True

    
    
    
    
    
    time.sleep(30)

client.close()
