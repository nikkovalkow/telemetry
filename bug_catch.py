import os
import datetime
while(1):

    data = os.popen('ping 8.8.8.8 -c 1').read()

    if data.find('1 received')!=-1:
        print("Ok")
    else:
        print("No internet",datetime.datetime.now())