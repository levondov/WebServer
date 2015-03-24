from googlevoice import Voice
from googlevoice.util import input

voice = Voice()
voice.login()

mess = "New Camera motion detected, check your email in a few minutes!"

mail_list = open('../../maillist.txt','r')
for line in mail_list:
	voice.send_sms(line,mess)
	if 'str' in line:
		break
