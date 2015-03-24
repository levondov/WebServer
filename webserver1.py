#!/usr/bin/env python

import socket
import sys
import subprocess
import time

HOST, PORT = '192.168.1.122', 8888

# create tcp/ip socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind socket to localhost and port
print 'Serving HTTP on port %s ...' % PORT
sock.bind((HOST, PORT))
sock.listen(1)

##global connection open or closed
con = 'open'

def request_options(data,connection):
	datasplit = data.split()
	if datasplit[0] == 'time':
		gettime(connection)
	elif datasplit[0] == 'wifi':
		getwifi(connection)
	elif len(datasplit) > 1 and datasplit[2] == 'HTTP/1.1':
		getpage(datasplit[1],connection)
	else:
		connection.sendall('no command found for \'' + data + '\' \n')

# return current time
def gettime(connection):
	global con
	con = 'open'
	time_resp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	connection.sendall(time_resp + '\n')

# return wifi strength
def getwifi(connection):
	global con
	con = 'open'
	proc = subprocess.check_output(['python wifi_strength.py'],shell=True)
	connection.sendall(proc + '\n')
	
def getpage(fname,connection):
	global con
	con = 'closed'
	try:
		f = open(fname[1:] + '.html')
		fout = f.read()
	
		connection.send('HTTP/1.1 200 OK\nContent-Type: text/html\n\n')
		for i in range(0, len(fout)):
			connection.send(fout[i])
		connection.close()
	except:
		f = open('noPage.html')
		fout = f.read()
		
		connection.send('HTTP/1.1 200 OK\nContent-Type: text/html\n\n')
		for i in range(0, len(fout)):
			connection.send(fout[i])
		connection.close()

def main():
	while True:
		# waiting for a connection
		print 'waiting for a connection...'
		connection, client_address = sock.accept()
		try:
			print 'connection from', client_address
		
			#recieve data and send back info
			while True:
				data = connection.recv(1492)
				# recv places 2 extra spaces at the end of data, remove this
				data = data[0:len(data)-2]
				print 'received: ', data

				if data:
					# save requests/time/client_address to text file
					curr_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
					request_file = open('requests.txt','a')
					request_file.write('\n' + curr_time + ' ' + data + ' ' + str(client_address[0]) + ' ' + str(client_address[1]))
					request_file.close()
					
					# Process the request and send a response to user.
					print 'Processing request...'
					request_options(data,connection)
					print 'Finished \n'
				else:
					print 'no more data from', client_address, 'closing connection'
					break

				#check connection
				if con == 'closed':
					break
		finally:
			#close and clean up connection
			connection.close()
			
main()
