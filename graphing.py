#!/usr/bin/python3
import numpy as np
from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file, save
from pymongo import MongoClient
import datetime
import cgitb
import cgi
import datetime

cgitb.enable()
print('Content-Type: text/html;charset=utf-8')
print('')
arguments=cgi.FieldStorage()
start=str(arguments.getfirst('start','Null')).split('.')
end=str(arguments.getfirst('end','Null')).split('.')

for i in range (len(start)+1,6):
        start.append('0')

for i in range (len(end)+1,6):
        end.append('0')

time_range=[]
time_range.append(start)
time_range.append(end)

for time_point in time_range:
        for i in range(0,len(time_point)):
                try:
                        time_point[i]=int(time_point[i])
                        if time_point[i]>10000: time_point[i]=0
                except:
                        time_point[i]=0

try:
        start = datetime.datetime(time_range[0][0],time_range[0][1],time_range[0][2],time_range[0][3],time_range[0][4])
except:
        start = datetime.datetime.now()
        print('Date paramenter error')
try:
        end = datetime.datetime(time_range[1][0],time_range[1][1],time_range[1][2],time_range[1][3],time_range[1][4])
except:
        end= datetime.datetime.now()
        print('Date paramenter error')


client = MongoClient('localhost',27017)

db = client['sensors']
col= db['temperature']

from_date = start
to_date = end

figures=[]

for sensor in range(0,5):
    timelist=[]
    templist=[]

    figures.append(figure(x_axis_type="datetime", title="Sensor "+str(sensor)))
    figures[sensor].grid.grid_line_alpha=0.3
    figures[sensor].xaxis.axis_label = 'Date'
    figures[sensor].yaxis.axis_label = 'Temp'
    
    for record in col.find({ 'time':{'$gte':from_date,'$lt':to_date},'sensor':sensor}):
        timelist.append(record['time'])
        templist.append(record['temp'])

    figures[sensor].line(timelist, templist, color='#33cc33', legend='Temperature')

timelist=[]
templist=[]

col= db['network']

internet = figure(x_axis_type="datetime", title="Internet")
internet.grid.grid_line_alpha=0.3
internet.xaxis.axis_label = 'Date'
internet.yaxis.axis_label = 'delay (ms)'

for record in col.find({ 'time':{'$gte':from_date,'$lt':to_date},'sensor':0}):
    
    timelist.append(record['time'])
    templist.append(record['ms-delay'])



internet.line(timelist, templist, color='#33cc33', legend='Internet_delay')
    
   

output_file("/var/www/html/data/sensors.html", title="Sensors")

figures_list=[]
for f in figures:
    figures_list.append([f])
figures_list.append([internet])

save(gridplot(figures_list, plot_width=1800, plot_height=400))

print('<a href=/data/sensors.html>Data for '+str(start)+' - '+str(end)+' </a>')
