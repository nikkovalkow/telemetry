import datetime

def GetSensorInfo(plot_num):
    #Description, Y-Name,Graph num,color
    try:
        switcher ={0:["Pi CPU",'Temp',3,'#33cc33'],1:["Oil Pump",'Temp',0,'#33cc33'],2:["Power Supply Oil",'Temp',0,'orange'],3:["ASIC Oil Out",'Temp',0,'skyblue'],4:['Internet delay','delay(ms)',2,'#33cc33']}
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


