import socket
import json
import sys

api_ip = '192.168.10.10'
api_port = 4028


def linesplit(socket):
        buffer = socket.recv(4096)
        done = False
        while not done:
                more = socket.recv(4096)
                if not more:
                        done = True
                else:
                        buffer = buffer+more
        if buffer:
                return buffer

def GetMinerInfo()

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((api_ip,int(api_port)))
    s.send(json.dumps({"command":'summary'}).encode())

    response = linesplit(s)

    response = response.decode('utf8')
    response = json.loads(response)

    mhs = int(response['SUMMARY'][0]['MHS 5s'])
    freq = int(response['SUMMARY'][0]['freq_avg'])
    voltage = int(response['SUMMARY'][0]['Voltage'])
    power = int(response['SUMMARY'][0]['Power'])
    temperature= int(response['SUMMARY'][0]['Temperature'])



    print(mhs,freq,temperature,voltage,power)
    s.close()

GetMinerInfo()
