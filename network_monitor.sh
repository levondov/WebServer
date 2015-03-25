#!/bin/bash

x=1
while true ; do
   if ifconfig wlan0 | grep -q "inet addr:" ; then
	if [ x = 0 ] ; then
		python /home/pi/WebServer/phone_notif_wifi2.py &
		x=1
	fi
      sleep 60
   else
     if [ x = 1 ] ; then
      	echo "Network connection down! Attempting reconnection..."
	x=0
     fi
      ifup --force wlan0
      sleep 10
   fi
done
