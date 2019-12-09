def GetCPUTemp():
    cpu_sensor= open('/sys/class/thermal/thermal_zone0/temp')
    return int(cpu_sensor.read())/1000

