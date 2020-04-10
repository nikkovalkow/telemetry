
import socket
import json

def linesplit(socket):
    buffer = socket.recv(4096)
    done = False
    while not done:
        more = socket.recv(4096)
        if not more:
            done = True
        else:
            buffer = buffer + more
    if buffer:
        return buffer


def GetWhatsMinerInfo(ip,port):

    try:

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, int(port)))
        s.send(json.dumps({"command": 'summary'}).encode())

        response = linesplit(s)

        response = response.decode('utf8').replace('\x00', '')
        response = json.loads(response)
        print(response)

    except:
         return [0, 0, 0, 0, 0]
GetWhatsMinerInfo('192.168.10.10',4028)