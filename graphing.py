#!/usr/bin/python3
from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file, save
from pymongo import MongoClient
import cgitb
import cgi
import datetime
from graphing_func import GetSensorInfo, ConvertStrToDate
import sys
import pandas as pd
from bokeh.models import DatetimeTickFormatter, HoverTool

#export_file_path = "/var/www/html/data/sensors.html"
number_of_sensors = 14
export_file_path = "sensors.html"

print(sys.argv)
from_date=ConvertStrToDate(str(sys.argv[1]))
to_date=ConvertStrToDate(str(sys.argv[2]))

scale  = sys.argv[3] # T , H , D, W, M
circles = sys.argv[4] #Y/N
export_file_path = sys.argv[5] #File path
# TEST ENV
#from_date=ConvertStrToDate('2019.12.13')
#to_date=ConvertStrToDate('2019.12.14')




client = MongoClient('localhost',27017)

db = client['sensors']
col= db['data']

figures=[]
figures_sensors={}

for i in range(0,number_of_sensors):
    figures.append(None)





for sensor in range(0,number_of_sensors):
    timelist=[]
    templist=[]
    sensor_info=GetSensorInfo(sensor)

    if figures[sensor_info[2]]==None:
        if (sensor == 0):
            figures[sensor_info[2]] = figure(x_axis_type="datetime")
        else:
            figures[sensor_info[2]] = figure(x_axis_type="datetime",x_range =  figures[GetSensorInfo(0)[2]].x_range)

        figures[sensor_info[2]].xaxis.axis_label = 'Date'
        figures[sensor_info[2]].yaxis.axis_label = sensor_info[1]
        figures[sensor_info[2]].ygrid.band_fill_alpha = 0.01
        figures[sensor_info[2]].ygrid.band_fill_color = "navy"


    for record in col.find({ 'time':{'$gte':from_date,'$lt':to_date},'sensor':sensor}):
        timelist.append(record['time'])
        templist.append(record['value'])

    if (len(timelist)!=0):
        frame = pd.DataFrame(templist,index=timelist)

        frame = frame[0].resample(scale, label='right', closed='right').mean()

        timelist = frame.index.tolist()
        templist = frame.tolist()

        figures[sensor_info[2]].line(timelist, templist, color=sensor_info[3],line_width=1.5,line_alpha=0.8,legend=sensor_info[0])
        if circles=="Y":
            figures[sensor_info[2]].square(x=timelist, y=templist)
            figures[sensor_info[2]].add_tools(HoverTool(tooltips=[("date", "@x{%F %H-%M}"),("value","$y")], formatters={"x": "datetime"}))
        figures[sensor_info[2]].legend.location = 'bottom_left'
        figures[sensor_info[2]].legend.orientation = "horizontal"
timelist=[]
templist=[]






figures_list=[]
for f in figures:
    if f!=None:
        figures_list.append([f])
output_file(export_file_path, title="Sensors")

save(gridplot(figures_list, plot_width=1800, plot_height=300))


