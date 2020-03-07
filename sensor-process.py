import RPi.GPIO as GPIO
from pymongo import MongoClient
import time
import datetime
from sendsms import SendSMS
from sensors_func import GetMinerInfo
from hw_platform import GetHDDSpace

import RPi.GPIO as GPIO
import dht11

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
instance = dht11.DHT11(pin = 26)
SmsIsSent=False

sensors=['28-030197945ffe','28-03029794645a', '28-030c97940c83']

def GetDHT11Temperature():
    try:
        for x in range(0,20):
            result = instance.read()
            if result.is_valid() and result.temperature!=0:
                return result.temperature
                break
            time.sleep(1)
        return -127
    except:
        print('DHT11 read error')
        return -127

def GetDHT11Humidity():
    try:
    
        for x in range(0,20):
            result = instance.read()
            if result.is_valid() and  result.humidity!=0:
                return result.humidity
                break
            time.sleep(1)
        return -127
    except:
        print('DHT11 read error')
        return -127        
    
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

def PutSensor(device,number,value,collection):
    try:
        testdata = {'time': datetime.datetime.now(),'device':device, 'sensor': number, 'value': value}
        collection.insert_one(testdata)
    except:
        print('PutSensor - error writing to db')


client = MongoClient('localhost',27017)

db = client['sensors']
col= db['data']

while 1:
    PutSensor(0,0,GetCPUTemp(),col)

    sensor_number=1

    for s in sensors:
        sensor_temperature = GetTemperatureDS18(s)
        PutSensor(0,sensor_number,sensor_temperature , col)
        sensor_number = sensor_number + 1

        if (sensor_temperature > 69) and not SmsIsSent:
            SendSMS('Sensor '+str(sensor_number)+' temperature '+str(sensor_temperature))
            #SendSMS('Hello world11')
            print ("Temperature warning!")
            SmsIsSent=True

    miner_info = GetMinerInfo()
    
    for v in miner_info:
        sensor_number = sensor_number + 1
        
        PutSensor(1,sensor_number, v, col)

    sensor_number = sensor_number + 1
    dht11_temp = GetDHT11Temperature()
    dht11_humidity = GetDHT11Humidity()
    if dht11_temp!=-127:
        PutSensor(0,sensor_number,dht11_temp,col)
    
    sensor_number = sensor_number + 1
    if dht11_humidity!=-127:
        PutSensor(0,sensor_number,dht11_humidity,col)

    sensor_number = sensor_number + 1
    PutSensor(0, sensor_number, GetHDDSpace(), col)

    time.sleep(30)

client.close()
