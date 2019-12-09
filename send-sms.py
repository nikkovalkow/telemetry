import os

def SendSMS(text):
    print(os.system('gammu sendsms TEXT +375296799727 -text "'+text+'"') )

SendSMS('Hello world')
    
