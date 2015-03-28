#!/usr/bin/env python

from twilio.rest import TwilioRestClient
import os

auth_codes = open('/home/pi/logs/twilio_auth.txt','r').readlines()
client = TwilioRestClient(auth_codes[0][0:len(auth_codes[0])-1],auth_codes[1][0:len(auth_codes[1])-1])

mess = "Camera motion detected. Stand by for images."
twilio_num = open('/home/pi/logs/twilio_num.txt','r').read()

mail_list = open('/home/pi/logs/maillist.txt','r')
#voice.send_sms('18183193707',mess)
for line in mail_list:
	message = client.messages.create(body=mess,to=line,from_=twilio_num)
	if 'str' in line:
		break
