#!/usr/bin/env python

# Using BeautifulSoup to extract messages through the html page
from googlevoice import Voice
from googlevoice.util import input
import time
import sys
import os
from bs4 import BeautifulSoup


def extractmsg(htmlpage):

	spanNum = []
	spanMes = []
	# Extract all conversations by searching for a DIV with an ID at top level.
	tree = BeautifulSoup(htmlpage)
	conv = tree.find_all('div', attrs={'id' : True}) # no recursive needed here
	
	# if conv is empty that means no new messages. we can break from the method
	if len(conv) == 0 :
		return spanNum, spanMes
		
	# since only the first element of conv has info in it, we ignore the rest of the list	
	# For each conversation, extract each row. Note each row contains 1 message
	rows = conv[0].find_all(attrs={'class' : 'gc-message-sms-row'})

	# For each row, grab the message and the phone number
	for i in range(0,len(rows)) :
		spanNum.append(rows[i].find_all('span', attrs={'class' : 'gc-message-sms-from'}))
		spanMes.append(rows[i].find_all('span', attrs={'class' : 'gc-message-sms-text'}))

	# Extract text from the spans
	for i in range(0,len(spanNum)) :
		spanNum[i] = spanNum[i][0].get_text()
		spanMes[i] = spanMes[i][0].get_text()
	
	# Remove all sent texts and keep only received ones
	spanNum_receive = []
	spanMes_receive = []
	for i in range(0,len(spanNum)) :
		if(spanNum[i].find('+') != -1) :
			# if there is a '+' in the number, then it is not from 'Me' but someone else
			spanNum_receive.append(spanNum[i][spanNum[i].find('+')+1:spanNum[i].find('+')+1+11])
			spanMes_receive.append(spanMes[i])

	return spanNum_receive,spanMes_receive

def init_sms_response_system():
	mail_list = open('../../maillist.txt','r')
	for line in mail_list:
		voice.send_sms(line,'Welcome to the raspberry pi sms response system. ' \
		'To see a list of possible commands reply back with \'help\' ' \
		'If you want to removed from this list please message levon')
		if 'str' in line:
			break

def savetofile(num,mes) :
	# check to see if input is empty. This means no new messages to write so break out of the method

	# save all received messages and their numbers
	request_file = open('sms_responses2.txt','a')
	for i in range (0,len(num)) :
		curr_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		request_file.write('\n' + num[i] + '-' + curr_time + ' ' + mes[i])
	request_file.close()

def processrequest(num,mes) :
	# read the sms and reply accordingly
	for i in range(0,len(num)):
		if (mes[i].lower().find('hi') != -1):
			voice.send_sms(num[i],'Hello, this is the raspberry pi')
		elif (mes[i].lower().find('stop') != -1 or mes[i].find('kill') != -1):
			os.system('kill -9 $(pidof motion)')
			voice.send_sms(num[i],'Motion has been turned off. Use \'restart\' to turn it back on')
		elif (mes[i].lower().find('restart') != -1):
			os.system('kill -9 $(pidof motion)')
			os.system('motion start')		
			voice.send_sms(num[i],'Motion has restarted.')
		elif (mes[i].lower().find('help') != -1):
			voice.send_sms(num[i],'I can handle the following commands: \n' \
			'help, kill/stop, restart, start webserver, start network monitor, and execute reboot (reboots me).')
		elif (mes[i].lower().find('execute reboot') != -1):
			os.system('reboot')
		elif (mes[i].lower().find('start webserver') != -1):
			try:
				os.system('python ../webserver1.py &')
				voice.send_sms(num[i],'WebServer initiated, find the homepage at http://192.168.1.122:8888/hello')
			except:
				voice.send_sms(num[i],'The WebServer is already running.')
		elif (mes[i].lower().find('start network monitor') != -1):
			try:
				os.system('./network_monitor.sh &')
                                voice.send_sms(num[i],'Network monitor turned on. If my wifi goes down I will message you.')
                        except:
                                voice.send_sms(num[i],'Network monitor is already on')
		elif(mes[i].lower().find('empty ') != -1):
			num_delete_days = mes[i][mes[i].lower().find('empty ')+6]
			cmdstring = 'find /media/networkshare/protected -mtime +%s -exec rm {} \;' % (num_delete_days)
			try:
				os.system(cmdstring)
				voice.send_sms(num[i],'Done!')
			except:
				voice.send_sms(num[i],'Sorry, something went wrong. See ~/WebServer/cam_stuff/sms_responses2.py' \
				'at line 100')

		else:
			voice.send_sms(num[i],'Sorry I didn\"t understand that command. Try again or reply \"help\"  to see my options')
def deletesms() :
	# after checking,replying, and saving messages, delete them on google voice
	for message in voice.sms().messages:
		message.delete()

# Login to google voice
global voice
voice = Voice()
voice.login()

# Initialize mailing list, send out a message to let people know system is up and running
init_sms_response_system()

# Check for new messages every minute
# if new message: process, reply, save, then delete message
while True:
	voice.sms()
	numbers, messages = extractmsg(voice.sms.html)
	
	savetofile(numbers,messages)
	processrequest(numbers,messages)
	deletesms()
	
	time.sleep(30)



