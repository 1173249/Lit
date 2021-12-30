#!/bin/bash

package=com.gitlab.ardash.appleflinger.android
previous=20

#for ((i = 10; i < 30; i+=20))
#do

cd /home/adminadmin/Desktop/Lab/bin/
#sed -i "s/numberoftestcases=$previous/numberoftestcases=$i/g" ../conf/config.ini
#previous=$i


./testcase_gen.py 
/home/adminadmin/Android/Sdk/platform-tools/adb shell pm grant $package android.permission.WRITE_EXTERNAL_STORAGE
#/home/adminadmin/Android/Sdk/platform-tools/adb shell am instrument -m $package/.test.JacocoInstrumentation&
sleep 10
cd /home/adminadmin/Desktop/Lab/bin/
timeout 60m python play.py
#cd -

#/home/adminadmin/Android/Sdk/platform-tools/adb shell input keyevent KEYCODE_APP_SWITCH
#/home/adminadmin/Android/Sdk/platform-tools/adb shell input  swipe 1600 1040 1600 200 100
#sleep 2
#/home/adminadmin/Android/Sdk/platform-tools/adb pull /sdcard/coverage.ec .
#mv coverage.ec coverage.ec.$i
#break
#done
