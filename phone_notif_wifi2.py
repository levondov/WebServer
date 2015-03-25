from googlevoice import Voice
from googlevoice.util import input

voice = Voice()
voice.login()

mess = "Wifi reconnection successful, restarting motion..."

mail_list = open('/home/pi/logs/maillist.txt','r')
for line in mail_list:
        voice.send_sms(line,mess)
        if 'str' in line:
                break

