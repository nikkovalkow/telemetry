import os
import datetime
import time


while(1):
    print("pinging 192.168")
    data = os.popen('ping 192.168.1.1 -c 1').read()
    print("complete")

    if data.find('1 received') == -1:
        print("No connection 192.168.1.1 ",datetime.datetime.now())
    print("pinging 8.8.8.8")

    data = os.popen('ping 8.8.8.8 -c 1').read()
    print("complete")

    if data.find('1 received') == -1:
        print("No connection 192.168.1.1 ",datetime.datetime.now())


