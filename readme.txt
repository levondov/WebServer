March 26
- added dropbox file support
	- images are uploaded after an event and then a share link is texted to anyone on the mailing list
- fixed minor bugs and problems.
- removed email support. No more emails will be sent w/ images/video
March 23
- added sms responses
	- i.e. You can txt the raspberry pi a cmd and it will process your request. See sms_responses.py in cam_stuff.
	- Used a python package called BeautifulSoup to extract sms messages from google voice. Since there is no direct api to grab messages, I grabbed the entire html page and processed the messages with BeautifulSoup

March 22
- added sms notification system using pygooglevoice
	- can't send mms right now. Notification gets sent when on_motion_detected
- added a wifi diagnostics script
	- bash script checks wifi every minute and if wifi is down, tries to reconnect
	- sms notification is also turned on for this
- changed file names apon save; it should be more readable now
- added files to github under WebServer

