import datetime
import os
import time
import sys


if sys.argv[1]=="2DAYS":

    now = datetime.datetime.now()
    begin = now - datetime.timedelta(days=1)
    now = now + datetime.timedelta(days=1)
    os.system("python3 graphing.py "+str(begin.year)+'.'+str(begin.month)+'.'+str(begin.day)+' '+str(now.year)+'.'+str(now.month)+'.'+str(now.day)+' 5T N sensors_2days.html')
    time.sleep(30)
    os.system('scp -o PubkeyAuthentication=yes  /var/www/html/data/sensors_2days.html root@learnin.ru:/var/www/html/sensors_2days.html')

if sys.argv[1]=="ALL":
    now = datetime.datetime.now()
    begin = now - datetime.timedelta(months=10)
    now = now + datetime.timedelta(days=1)
    os.system("python3 graphing.py " + str(begin.year) + '.' + str(begin.month) + '.' + str(begin.day) + ' ' + str(now.year) + '.' + str(now.month) + '.' + str(now.day) + ' W Y sensors_weekly.html')
    time.sleep(30)
    os.system('scp -o PubkeyAuthentication=yes  /var/www/html/data/sensors_weekly.html root@learnin.ru:/var/www/html/sensors_weekly.html')
    
if sys.argv[1]=="2MONTHS":
    now = datetime.datetime.now()
    begin = now - datetime.timedelta(months=2)
    now = now + datetime.timedelta(days=1)
    os.system("python3 graphing.py " + str(begin.year) + '.' + str(begin.month) + '.' + str(begin.day) + ' ' + str(now.year) + '.' + str(now.month) + '.' + str(now.day) + ' D Y sensors_daily.html')
    time.sleep(30)
    os.system('scp -o PubkeyAuthentication=yes  /var/www/html/data/sensors_daily.html root@learnin.ru:/var/www/html/sensors_daily.html')
