# Using BeautifulSoup to extract messages through the html page
from googlevoice import Voice
from googlevoice.util import input
import time
import sys
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
		if (mes[i].find('hi') != -1 or mes[i].find('Hi') != -1):
			voice.send_sms(num[i],'Hello, this is the raspberry pi')

def deletesms() :
	# after checking,replying, and saving messages, delete them on google voice
	for message in voice.sms().messages:
		message.delete()

# Login to google voice
global voice
voice = Voice()
voice.login()


# Check for new messages every minute
# if new message: process, reply, save, then delete message
while True:
	voice.sms()
	numbers, messages = extractmsg(voice.sms.html)
	
	savetofile(numbers,messages)
	processrequest(numbers,messages)
	deletesms()
	
	time.sleep(30)



