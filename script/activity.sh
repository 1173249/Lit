#!/bin/bash

rm coverage.activity
while true
do
	/home/adminadmin/Android/Sdk/platform-tools/adb shell dumpsys activity activities | grep 'Hist #' >> coverage.activity
	sleep 1 
done

