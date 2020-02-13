import os
import datetime
import time
def PingTest(ip):
    data = os.popen('ping '+ip+' -c 1').read()

    if data.find('1 received') != -1:
        return True
    else:
        return False


while(1):
    print("192.168.0.1" ,PingTest("192.168.0.1"),datetime.datetime.now())
    print("8.8.8.8", PingTest("8.8.8.8"),datetime.datetime.now())

    time.sleep(1)