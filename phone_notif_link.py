#file="phone_notif_link.py"
#!/usr/bin/env python
from googlevoice import Voice
import os, sys, time, subprocess
import argparse
from stat import S_ISREG, ST_CTIME, ST_MODE


parser = argparse.ArgumentParser()
parser.add_argument( '-s')
args= parser.parse_args()

def send_link(link):

	voice = Voice()
	voice.login()
	
	mail_list = open('/home/pi/logs/maillist.txt','r')
	#voice.send_sms('18183193707',link)
	for line in mail_list:
	        voice.send_sms(line,link)
	        if 'str' in line:
	                break
def find_recent():
	
	dirpath = '/media/networkshare/protected/'
	# get all entries in the directory w/ stats
	entries = (os.path.join(dirpath, fn) for fn in os.listdir(dirpath))
	entries = ((os.stat(path), path) for path in entries)
	entries = ((stat[ST_CTIME], path) for stat, path in entries if S_ISREG(stat[ST_MODE]))
	#for cdate, path in sorted(entries):
    	#	print time.ctime(cdate), os.path.basename(path)	
	return sorted(entries)[-1][1]

def upload_share(path):
	# first upload
	cmd = './dropbox_uploader.sh upload %(fullpath)s /RaspberryPi_cam/%(relpath)s &' % { 'fullpath': path, 'relpath': os.path.basename(path) }
	os.system(cmd)
	# wait a few seconds for dropbox to update
	time.sleep(10)
	# share
	cmd = './dropbox_uploader.sh share /RaspberryPi_cam/%s & ' % os.path.basename(path)
	return subprocess.check_output(cmd, shell=True)


# wait for the camera to save the jpg/video
#time.sleep(5)
# Find the most recent image
dir_path = find_recent()
# upload and share the image on dropbox
share_link = upload_share(dir_path)
# send image link as sms
send_link(share_link)
