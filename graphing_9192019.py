import numpy as np
from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file
from pymongo import MongoClient
import datetime


p1 = figure(x_axis_type="datetime", title="Room Temperature")
p1.grid.grid_line_alpha=0.3
p1.xaxis.axis_label = 'Date'
p1.yaxis.axis_label = 'Temp'


p2 = figure(x_axis_type="datetime", title="CPU Temperature")
p2.grid.grid_line_alpha=0.3
p2.xaxis.axis_label = 'Date'
p2.yaxis.axis_label = 'Temp'


client = MongoClient('localhost',27017)

db = client['sensors']
col= db['temperature']

from_date = datetime.datetime(2019,9,14,9,10,30)
to_date = datetime.datetime(2019,9,19,10,40,30)
timelist=[]
templist=[]


for record in col.find({ 'time':{'$gte':from_date,'$lt':to_date},'sensor':1}):
    timelist.append(record['time'])
    templist.append(record['temp'])


p1.line(timelist, templist, color='#FF6A33', legend='Room temperature')

p1.legend.location = "top_left"

timelist=[]
templist=[]

for record in col.find({ 'time':{'$gte':from_date,'$lt':to_date},'sensor':0}):
    timelist.append(record['time'])
    templist.append(record['temp'])


p2.line(timelist, templist, color='#33cc33', legend='CPU Temperature')


output_file("temperature.html", title="Temp sensors")

show(gridplot([[p1],[p2]], plot_width=1800, plot_height=400))
