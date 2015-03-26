#!/usr/bin/env python

from googlevoice import Voice
import os

voice = Voice()
voice.login()

mess = "Camera motion detected. Stand by for images."

mail_list = open('/home/pi/logs/maillist.txt','r')
#voice.send_sms('18183193707',mess)
for line in mail_list:
	voice.send_sms(line,mess)
	if 'str' in line:
		break
