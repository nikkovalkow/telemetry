import socket
import time
from timeit import default_timer
from pymongo import MongoClient
import datetime

try:
    client = MongoClient('localhost',27017)

    db = client['sensors']
    col= db['network']
except:
    print ("Check_Internet - mongodb connection error")


def TestInternetConnection():

    start = 0
    end = 0
    try:
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        start = default_timer()
        s.connect(('8.8.8.8',53))
        end = default_timer()
        s.close()

        return round((end-start)*1000,1)
    except:

        return 0


for repeat in range(0,2):
  
    testdata={ 'time':datetime.datetime.now(),'sensor':0,'ms-delay' : TestInternetConnection() }
    col.insert_one(testdata)
    time.sleep(30)
