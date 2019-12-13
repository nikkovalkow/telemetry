import os

def SendSMS(text):
    
    print('sending')
    os.system('sudo iptables -A FORWARD -s 192.168.10.10 -j DROP')
    print(os.system('gammu sendsms TEXT +375296799727 -text "'+text+'"') )
    print('')



    
