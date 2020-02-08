import datetime

def GetSensorInfo(plot_num):
    #Description, Y-Name,Graph num,color
    try:
        switcher ={0:["Pi CPU",'Temp',7,'#33cc33'],1:["Oil Pump",'Temp',0,'#33cc33'],2:["Power Supply Oil",'Temp',0,'orange'],3:["ASIC Oil Out",'Temp',0,'skyblue'],\
                   4:['Internet delay','delay(ms)',2,'#33cc33'],5:['MHS 5s','MHS 5s',3,'#33cc33'],6:['freq_avg','MHz',4,'#33cc33'],7:['Board temperature','Temp',0,'indianred'],\
                   8:['Voltage','V',5,'#33cc33'],9:['Power','W',6,'#33cc33'],10:['Efficiency','MH/W',8,'#33cc33'],11:['Temperature','C',1,'orange'],12:['Humidity','%',1,'skyblue'],\
                   13:['HDD space','%',9,'#33cc33']}
        return switcher.get(plot_num)
    except:

        return "Name error"


def ConvertStrToDate(str_time):

    try:
        return datetime.datetime.strptime(str_time,'%Y.%m.%d')
    except:
        try:
            return datetime.datetime.strptime(str_time, '%Y.%m.%d.%H.%M')
        except:
            return datetime.datetime.now()


