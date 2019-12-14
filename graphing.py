#!/usr/bin/python3
from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file, save
from pymongo import MongoClient
import cgitb
import cgi
import datetime
from graphing_func import GetSensorInfo, ConvertStrToDate

export_file_path = "/var/www/html/data/sensors.html"
#export_file_path = "sensors.html"


cgitb.enable()
print('Content-Type: text/html;charset=utf-8')
print('')
arguments=cgi.FieldStorage()

from_date=ConvertStrToDate(str(arguments.getfirst('start','Null')))
to_date=ConvertStrToDate(str(arguments.getfirst('end','Null')))


# TEST ENV
#from_date=ConvertStrToDate('2019.12.13')
#to_date=ConvertStrToDate('2019.12.14')




client = MongoClient('localhost',27017)

db = client['sensors']
col= db['temperature']

figures=[]
figures_sensors={}

for i in range(0,5):
    figures.append(None)





for sensor in range(0,4):
    timelist=[]
    templist=[]
    sensor_info=GetSensorInfo(sensor)

    if figures[sensor_info[2]]==None:
        figures[sensor_info[2]] =figure(x_axis_type="datetime")
        figures[sensor_info[2]].xaxis.axis_label = 'Date'
        figures[sensor_info[2]].ygrid.band_fill_alpha = 0.01
        figures[sensor_info[2]].ygrid.band_fill_color = "navy"


    for record in col.find({ 'time':{'$gte':from_date,'$lt':to_date},'sensor':sensor}):
        timelist.append(record['time'])
        templist.append(record['temp'])

    figures[sensor_info[2]].line(timelist, templist, color=sensor_info[3],line_width=1.5,line_alpha=0.8,legend=sensor_info[0])
    figures[sensor_info[2]].legend.location = 'bottom_left'
    figures[sensor_info[2]].legend.orientation = "horizontal"
timelist=[]
templist=[]




output_file(export_file_path, title="Sensors")

figures_list=[]
for f in figures:
    if f!=None:
        figures_list.append([f])


save(gridplot(figures_list, plot_width=1800, plot_height=400))

print('<a href=/data/sensors.html>Data for '+str(from_date)+' - '+str(to_date)+' </a>')
