import os
import datetime
import time


while(1):
    try:

        data = os.popen('ping 192.168.1.1 -c 1').read()


        if data.find('1 received') == -1:
            print("No connection 192.168.1.1 ",datetime.datetime.now())


        data = os.popen('ping 8.8.8.8 -c 1').read()


        if data.find('1 received') == -1:
            print("No connection 8.8.8.8 ",datetime.datetime.now())

        time.sleep(1)
    except:
        print("Error in bug_catch.py")


