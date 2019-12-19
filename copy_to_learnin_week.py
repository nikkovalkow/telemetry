import datetime
import os
import time
now = datetime.datetime.now()
begin = now - datetime.timedelta(days=7)
os.system("curl "+'\"http://192.168.1.110/graphing.py?start='+str(begin.year)+'.'+str(begin.month)+'.'+str(begin.day)+'&end='+str(now.year)+'.'+str(now.month)+'.'+str(now.day+1)+'\"')
time.sleep(30)
os.system('scp -o PubkeyAuthentication=yes  /var/www/html/data/sensors.html root@learnin.ru:/var/www/html/sensors_week.html')
