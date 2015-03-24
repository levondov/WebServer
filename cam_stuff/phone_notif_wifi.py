from googlevoice import Voice
from googlevoice.util import input

voice = Voice()
voice.login()

mess = "Raspberrypi wifi down, attempting to reconnect..."

mail_list = open('../../maillist.txt','r')
for line in mail_list:
        voice.send_sms(line,mess)
        if 'str' in line:
                break


