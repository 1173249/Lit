#!/usr/bin/env python
import sys
import copy
sys.path.append('../')
import subprocess
import configparser
import os
from adblibs import adb
import codecs
import json

def getConfigure():
    root_dir = os.path.dirname(os.path.abspath('.'))
    print (root_dir)
    cf = configparser.ConfigParser()
    cf.read(root_dir+"/conf/config.ini")     
    secs = cf.sections() 
    return cf

def getResolution():
    cmd = 'adb shell getevent -p'
    (status, output) = subprocess.getstatusoutput(cmdpath+ '\\' + cmd)
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
            
def getSize():
    cmd = 'adb shell wm size'
    (status, output) = subprocess.getstatusoutput(cmdpath+ '\\' + cmd)
    if status != 0:
        print("error fail to get size")
    output = output.strip()
    columns = output.split(": ")
    parts = columns[1].split("x")
    sizeX = parts[0]
    sizeY = parts[1]
    return [sizeX, sizeY]
    

def processLog(filename = "log.txt"):
    minX, maxX, minY, maxY = resolution[:]
    sizeX, sizeY = size[:]
    count = 0
    timestamp = '.'.join(filename.split('.')[-2:])
    
    with open (filename) as pf:
        lines = pf.readlines()
        Action = 'None'
        numberOfXY = 0
        startX = None
        startY = None
        startT = None
        endT = None
        endX = None
        endY = None
        traceSet["sequence"] = []
        if (len(lines) < 1):
            return

        for line in lines:
            line = line.strip()
        #print (line)
            columns = line.split(' ')
            if line.find("ABS_MT_TRACKING_ID") != -1:
                tracking_id = columns[-1]
                if (tracking_id != "ffffffff"):
                    Action='Start'
                    if startT == None:
                        tempcolumns = line.split(']')
                        startT = tempcolumns[0]

                if (tracking_id == "ffffffff" and startT != None):
                    Action='End'
                    if endT == None:
                        tempcolumns = line.split(']')
                        endT = tempcolumns[0]
                if (tracking_id == "ffffffff" and startT == None): # with incomplete log info
                    return
                    
            if Action == 'Start':
                if line.find("ABS_MT_POSITION_X") != -1:
                    x = columns[-1]
                    numberOfXY += 1
                    if startX == None:
                        startX = x

                if line.find("ABS_MT_POSITION_Y") != -1:
                    y = columns[-1]
                    numberOfXY += 1
                    if startY == None:
                        startY = y

            if Action == 'End':
                trace={}
                Action = 'None'
                endX = x
                endY = y
                if (startX == None or startY == None):
                    continue
                startX = int((int(startX, 16) - int(minX)) * int(sizeX) / (int(maxX) - int(minX)))
                startY = int((int(startY, 16) - int(minY)) * int(sizeY) / (int(maxY) - int(minY)))
                rotation = cf.get(gameName, "screenRotation")
                if (rotation == '0'):
                    temp = startX
                    startX = startY
                    startY = int(sizeX) - temp
                startT = startT.strip('[').strip(' ')
                endT = endT.strip('[').strip(' ')
                duration = float(endT) - float(startT)
                if (numberOfXY < 4 or duration < 0.2):
                    #print("tap   [" + str(startX) + " " + str(startY) + "]" )
                    traceSet["actions"].append({"type":"tap", "startX":startX, 
                        "startY":startY, "duration":duration, "timestamp":timestamp})
                    traceSet["sequence"].append("tap")
                else:
                    endX = int((int(endX, 16) - int(minX)) * int(sizeX) / (int(maxX) - int(minX)))
                    endY = int((int(endY, 16) - int(minY)) * int(sizeY) / (int(maxY) - int(minY)))
                    if (rotation == '0'):
                        temp = endX
                        endX = endY
                        endY = int(sizeX) - temp 
                    traceSet["actions"].append({"type":"swipe", "startX":startX, 
                        "startY":startY, "endX":endX, "endY":endY, 
                        "duration":duration, "timestamp":timestamp})
                    traceSet["sequence"].append("swipe")
                numberOfXY = 0
                startX = None
                startY = None
                endX = None
                endY = None
                startT = None
                endT = None
                #return

def dump2File(outfilename, traceSet):
    if ( not traceSet):
        return
    out = codecs.open(outfilename, 'w', 'utf8')
    out.write(json.dumps(traceSet, indent = 4, sort_keys=True, ensure_ascii=False))
    out.close()
                                        #logger.info("Done.")
def processTrace(traceDir, traceName):
    files = os.listdir(traceDir)
    for filename in files:
        if filename.find(traceName) != -1:
            print (filename)
            processLog(traceDir+'/'+filename)


def processPlayerTrace(traceDir, traceName, player):
    files = os.listdir(traceDir+player)
    for filename in files:
        if filename.find(traceName) != -1:
            print (filename)
            processLog(traceDir+player + '/'+filename, player)


if __name__ == "__main__":
    cf = getConfigure()
    cmdpath = cf.get("system", "cmdpath")
    gameName = cf.get("system", "gameName")
    traceName = cf.get(gameName, "tracefile")
    traceDir = cf.get(gameName, "dir")
    multiplayer = cf.get(gameName, "multiplayermode")
    device = cf.get("system", "device")
    
    adbkit = adb.adbKit(device)

    resolution = adbkit.getResolution()
    size = adbkit.getSize()

    
    if multiplayer == '1':
        playerIcons = cf.get(gameName, "playIcons")
        players = playerIcons.split(',')
        for player in players:
            traceSet = {}
            traceSet["actions"] = []
            processTrace(traceDir+player+'/trace/playicon/', traceName)
            actionfile = cf.get(gameName, "actionfile")
            dump2File(traceDir+player+'/'+actionfile, traceSet)

    else:
        traceSet = {}
        traceSet["actions"] = []
        processTrace(traceDir+'trace/playicon/', traceName)
        actionfile = cf.get(gameName, "actionfile")
        dump2File(traceDir+actionfile, traceSet)

        traceSet = {}
        traceSet["actions"] = []
        processTrace(traceDir+'trace/function/', traceName)
        actionfile = cf.get(gameName, "functionfile")
        dump2File(traceDir+actionfile, traceSet)
