#!/usr/bin/env python
# coding=utf-8

"""ADB"""

adb_path='/home/adminadmin/Android/Sdk/platform-tools'


import subprocess
import os
import signal
import time
import psutil


class adbKit(object):
    def __init__(self, devicename):
        self.device = devicename

    def screenshots(self, gamename, serialNumber=None):
        if serialNumber == None:
            os.system('adb exec-out screencap -p > ../image/'+gamename+'/screencap.png')
            return '../image/'+gamename+'/screencap.png'
        else:
            os.system('adb exec-out screencap -p > ../image/'+gamename+'/screencap.png.'+serialNumber)
            return '../image/'+gamename+'/screencap.png'+'.'+serialNumber

    def click(self, point, serialNumber=None):
        if (len(point) < 2):
            return
        return os.system('adb shell input tap '+str(point[0])+' '+str(point[1]))#, serialNumber)

    def swipe(self, point, point_end, duration=1000):
        if (len(point) < 2):
            return
        return self.command('shell input swipe ' + str(point[0])+' '+str(point[1])+' '+ str(point_end[0])+' '+str(point_end[1])+' '+str(duration) )
    
    def processcommand(self, cmd):
        cmdstr = adb_path+'/adb '
        if self.device is not None:
            cmdstr = cmdstr + ' -s ' + self.device + ' '
        pro = subprocess.Popen(cmdstr+cmd, shell=True)
        return pro

    def command(self, cmd, serialNumber=None):
        cmdstr = adb_path+'/adb '
        #print self.device
        if self.device is not None:
            cmdstr = cmdstr + ' -s ' + self.device + ' '
        if serialNumber:
            cmd = cmd+'.'+serialNumber
        #print cmdstr+cmd
        (status, output) = subprocess.getstatusoutput(cmdstr+cmd)
        return [status, output]

    def terminateCommand(self, pid):
        parent = psutil.Process(pid)
        for child in parent.children(recursive=True):  # or parent.children() for recursive=False
            child.kill()
        parent.kill()
        #os.kill(pid, signal.SIGTERM)

    def getevent(self, tracefile):
        #print 'getevent'
        cmdstr = 'exec-out getevent -lt >> ' + tracefile
        pro = self.processcommand(cmdstr)
        time.sleep(12)
        self.terminateCommand(pro.pid)
        print ("terminate")
        return


    def hasdevice(self):
        cmdstr = 'devices'
        (status, output) = subprocess.getstatusoutput(cmdstr)
        if (len(output) < 30):
            return False
        else:
            return True

    def setdevice(self, cf):
        if cf.has_option('system', "device"):
            self.decive = cf.get('system', "device")
        else:
            self.device = None

    def getResolution(self):
        cmd = 'adb shell getevent -p'
        (status, output) = subprocess.getstatusoutput(cmd)
        if status != 0:
            print("error fail to get resolution")
        lines = output.split('\n')
        for line in lines:
        #print (line)
            if line.find("0035  : ") != -1:
                line = line.strip()
                columns = line.split(",")
                minX = columns[1][5:]
                maxX = columns[2][5:]

            if line.find("0036  : ") != -1:
                line = line.strip()
                columns = line.split(",")
                minY = columns[1][5:]
                maxY = columns[2][5:]

        return [minX, maxX, minY, maxY]

    def getSize(self):
         cmd = 'adb shell wm size'
         (status, output) = subprocess.getstatusoutput(cmd)
         if status != 0:
            print("error fail to get size")
         output = output.strip()
         columns = output.split(": ")
         parts = columns[1].split("x")
         sizeX = parts[0]
         sizeY = parts[1]
         return [sizeX, sizeY]
