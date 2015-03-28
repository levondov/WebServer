#!/bin/bash

x=1
while true ; do
   if ifconfig wlan0 | grep -q "inet addr:" ; then
	echo "Reconnection Successful"
	sleep 60
   else
	echo "Network connection down! Attempting reconnection..."
	ifup --force wlan0
	sleep 10
	python wifi_outage.py
   fi
done
