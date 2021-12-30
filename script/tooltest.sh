#!/bin/bash

#package=com.plter.linkgame
#device=HT74C0200829

round=1
package=com.gitlab.ardash.appleflinger.android
device=emulator-5554
apk=apple-debug.apk
#candy-debug.apk

for ((i = 0; i < round; i++))
do
	echo $i
	/home/adminadmin/Android/Sdk/platform-tools/adb -s $device  uninstall $package
	/home/adminadmin/Android/Sdk/platform-tools/adb -s $device  install $apk
	/home/adminadmin/Android/Sdk/platform-tools/adb -s $device shell pm grant $package android.permission.WRITE_EXTERNAL_STORAGE
	/home/adminadmin/Android/Sdk/platform-tools/adb -s $device shell am start -n $package/.AndroidLauncher
	#com.jeupoo.activities.MainActivity
	python /home/adminadmin/Desktop/Lab/bin/play.py&

	sleep 40m 
#/home/adminadmin/Android/Sdk/platform-tools/adb -s $device exec-out screencap -p > screencap.$package.$i.10m.png
#/home/adminadmin/Android/Sdk/platform-tools/adb -s $device shell am broadcast -a vt.edu.jacoco.COLLECT_COVERAGE -p $package
#/home/adminadmin/Android/Sdk/platform-tools/adb -s $device pull /sdcard/coverage.ec .
#mv coverage.ec coverage.$package.$i.10m.exec

#sleep 20m

#/home/adminadmin/Android/Sdk/platform-tools/adb -s $device exec-out screencap -p > screencap.$package.$i.30m.png
#/home/adminadmin/Android/Sdk/platform-tools/adb -s $device shell am broadcast -a vt.edu.jacoco.COLLECT_COVERAGE -p $package
#/home/adminadmin/Android/Sdk/platform-tools/adb -s $device pull /sdcard/coverage.ec .
#mv coverage.ec coverage.$package.$i.30m.exec
#sleep 300m

/home/adminadmin/Android/Sdk/platform-tools/adb -s $device exec-out screencap -p > screencap.$package.$i.5h.png
/home/adminadmin/Android/Sdk/platform-tools/adb -s $device shell am broadcast -a vt.edu.jacoco.COLLECT_COVERAGE -p $package
/home/adminadmin/Android/Sdk/platform-tools/adb -s $device pull /sdcard/coverage.ec .
mv coverage.ec ../coverage/coverage.$package.$i.1h.exec

killall python
#mv ../data/candycrush ../data/candycrush.10m
#mv ../data/candycrush.6m ../data/candycrush
#pid=`/home/adminadmin/Android/Sdk/platform-tools/adb  -s emulator-5554 shell ps | grep monkey | awk '{print $2}'`
#/home/adminadmin/Android/Sdk/platform-tools/adb -s $device shell kill $pid
done

adb logcat -b crash > ../crash/log.txt
