import os


def SendSMS(text):
    print('sending')
    os.system('sudo iptables -A FORWARD -s 192.168.10.10 -j DROP')
    print(os.system('gammu sendsms TEXT +375296799727 -text "' + text + '"'))
    print('')

def GetHDDSpace():
    try:
        data = os.popen('df -h --output=source,pcent | grep root').read()
    
        return int(data.split(' ')[-1].replace('%',''))
    except:
        print('Error GetHDDSpace()')

def GetDS18List():






