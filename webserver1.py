import socket
import sys
import time

HOST, PORT = '', 8888


# create tcp/ip socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind socket to localhost and port
print 'Serving HTTP on port %s ...' % PORT
sock.bind((HOST, PORT))
sock.listen(1)

def request_options(data):
	if data == 'time':
		return (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
	else:
		return 'no command found for \'' + data + '\''

while True:
	# waiting for a connection
    print 'waiting for a connection...'
    connection, client_address = sock.accept()
    try:
    	print 'connection from', client_address
    
    	#recieve data and send back info
    	while True:
    		data = connection.recv(1024)
    		# recv places 2 extra spaces at the end of data, remove this
    		data = data[0:len(data)-2]
    		print 'received: ', data

    		if data:
    			# save requests/time/client_address to text file
    			curr_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    			request_file = open('requests.txt','a')
    			request_file.write('\n' + curr_time + ' ' + data + ' ' + str(client_address[0]) + ' ' + str(client_address[1]))
    			request_file.close()
    			
    			response = request_options(data)
    			
    			# send a message back to the user
    			print 'sending response to user \n'
    			connection.sendall(response + '\n')
    		else:
    			print 'no more data from', client_address
    			break
    finally:
    	#close and clean up connection
    	connection.close()
