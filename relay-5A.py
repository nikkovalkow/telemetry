import RPi.GPIO as GPIO
from pymongo import MongoClient
import time
import datetime

def GetTemperature():
    device = open('/sys/bus/w1/devices/28-030c97940c83/w1_slave','r')
    output = device.read()
    if output.find('YES')!=-1:
        return int(output[output.find('t=')+2:])/1000

def TestRelay():
    GPIO.setmode(GPIO.BCM)

    print ('test')
    NUM=15

    GPIO.setup(NUM,GPIO.OUT)
    GPIO.output(NUM,GPIO.LOW)
    time.sleep(2)
    GPIO.output(NUM,GPIO.HIGH)
    time.sleep(2)
    GPIO.output(NUM,GPIO.LOW)
    GPIO.cleanup()

    time.sleep(2)

    print(NUM)
def TempLoop():
    t=0
    while 1:
        if t!=GetTemperature():
            print (GetTemperature())
            t=GetTemperature()


client = MongoClient('localhost',27017)

db = client['sensors']
col= db['temperature']

while 1:
    time.sleep(30)
    testdata={ 'time':datetime.datetime.now(),'sensor':1,'temp' : GetTemperature() }
    print(testdata)
    col.insert_one(testdata)

client.close()
