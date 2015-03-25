import time

# save requests/time/client_address to text file
curr_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
request_file = open('wifi_outage.txt','a')
request_file.write('\n' + curr_time)
request_file.close()
