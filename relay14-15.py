import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

print ('test')
NUM=14

GPIO.setup(NUM,GPIO.OUT)
GPIO.output(NUM,GPIO.LOW)
GPIO.setup(NUM+1,GPIO.OUT)
GPIO.output(NUM+1,GPIO.LOW)



while 1:
    
    time.sleep(2)
    GPIO.output(NUM,GPIO.HIGH)
    time.sleep(2)
    GPIO.output(NUM,GPIO.LOW)

    time.sleep(2)
    GPIO.output(NUM+1,GPIO.HIGH)
    time.sleep(2)
    GPIO.output(NUM+1,GPIO.LOW)


GPIO.cleanup()

time.sleep(2)
