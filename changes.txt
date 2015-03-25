If the server ip address changes then go to and edit /etc/fstab with the new ip address.

If you want to change motion detection settings, go to /etc/motion/motion.conf and edit.


To get text message system working with pygooglevoice I changed the following:

in /usr/local/lib/python2.7/dist-packages/pygooglevoice-0.5-py2.7.egg/googlevoice/settings.py
we changed LOGIN to 'https://accounts.google.com/ServiceLogin?service=code&ltmpl=phosting&continue=http%3A%2F%2Fcode.google.com%2Fp%2Fpygooglevoice%2Fissues%2Fdetail%3Fid%3D64&followup=http%3A%2F%2Fcode.google.com%2Fp%2Fpygooglevoice%2Fissues%2Fdetail%3Fid%3D64'
See: https://code.google.com/p/pygooglevoice/issues/detail?id=64

also in voice.py we changed the following:
# holy hackjob
galx = re.search(r"name=\"GALX\"\s+type=\"hidden\"\s+value=\"(.+)\"", content).group(1)
See: https://code.google.com/p/pygooglevoice/issues/detail?id=76
