import os

def SendSMS(text):
    
    print('sending')
    print(os.system('gammu sendsms TEXT +375296799727 -text "'+text+'"') )
    print('')



    
