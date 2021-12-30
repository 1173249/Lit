#!/bin/bash

#package=in.game.starmagic
#device=HT74C0200829
round=5
package=com.gitlab.ardash.appleflinger.android
device=emulator-5554

for ((i = 0; i < round; i++))
do
	echo $i
/home/adminadmin/Android/Sdk/platform-tools/adb -s $device  uninstall $package
/home/adminadmin/Android/Sdk/platform-tools/adb -s $device  install android-debug.apk 
/home/adminadmin/Android/Sdk/platform-tools/adb -s $device shell pm grant $package android.permission.WRITE_EXTERNAL_STORAGE
#i/home/adminadmin/Android/Sdk/platform-tools/adb -s $device shell am start -n com.oldenweb.Archery/.Main
/home/adminadmin/Android/Sdk/platform-tools/adb -s $device shell monkey -v -v -v --throttle 4000  -p $package  15000 &

sleep 10m
/home/adminadmin/Android/Sdk/platform-tools/adb -s $device exec-out screencap -p > screencap.$package.10m.png.$i
/home/adminadmin/Android/Sdk/platform-tools/adb -s $device shell am broadcast -a vt.edu.jacoco.COLLECT_COVERAGE -p $package
/home/adminadmin/Android/Sdk/platform-tools/adb -s $device pull /sdcard/coverage.ec .
mv coverage.ec coverage.$package.10m.$i.exec

sleep 20m
/home/adminadmin/Android/Sdk/platform-tools/adb -s $device exec-out screencap -p > screencap.$package.30m.png.$i
/home/adminadmin/Android/Sdk/platform-tools/adb -s $device shell am broadcast -a vt.edu.jacoco.COLLECT_COVERAGE -p $package
/home/adminadmin/Android/Sdk/platform-tools/adb -s $device pull /sdcard/coverage.ec .
mv coverage.ec coverage.$package.30m.$i.exec

sleep 30m
/home/adminadmin/Android/Sdk/platform-tools/adb -s $device exec-out screencap -p > screencap.$package.1h.png.$i
/home/adminadmin/Android/Sdk/platform-tools/adb -s $device shell am broadcast -a vt.edu.jacoco.COLLECT_COVERAGE -p $package
/home/adminadmin/Android/Sdk/platform-tools/adb -s $device pull /sdcard/coverage.ec .
mv coverage.ec coverage.$package.1h.$i.exec


pid=`/home/adminadmin/Android/Sdk/platform-tools/adb  -s emulator-5554	 shell ps | grep monkey | awk '{print $2}'`
/home/adminadmin/Android/Sdk/platform-tools/adb -s $device shell kill $pid

done
