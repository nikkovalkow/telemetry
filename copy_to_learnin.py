import datetime
import os
import time
now = datetime.datetime.now()
os.system("curl "+'\"http://192.168.1.110/graphing.py?start='+str(now.year)+'.'+str(now.month)+'.'+str(now.day-1)+'&end='+str(now.year)+'.'+str(now.month)+'.'+str(now.day+1)+'\"')
time.sleep(20)
os.system('scp -o PubkeyAuthentication=yes  /var/www/html/data/sensors.html root@learnin.ru:/var/www/html')
