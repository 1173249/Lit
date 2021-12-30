#!/usr/bin/env python
# coding=utf-8

adb_path='/home/adminadmin/Android/Sdk/platform-tools'
logfile='../log/command.log'
#import commands
import sys, time
sys.path.append('../')
import cv2
import numpy as np
import logging
import random
from adblibs import adb
from screenlibs import screen
from time import gmtime, strftime
import configparser
import os
import json
import numpy
from sympy import *
from contextlibs import contextarray
import copy

def getConfigure():
    root_dir = os.path.dirname(os.path.abspath('.'))
    logger.info (root_dir)
    cf = configparser.ConfigParser()
    cf.read(root_dir+"/conf/config.ini")     
    secs = cf.sections() 
    return cf

def Init():
    formatter_str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    log_level = logging.DEBUG
    logging.basicConfig(filename=logfile, format=formatter_str, level=log_level)
    logger = logging.getLogger(__name__)
    return logger

def loadTestcase():
    testcaseSet = {}
    testcasefile = cf.get(gamename, "testcasefile")
    if multiplayer == '1':
        players = playerIcons.split(',')
        for player in players:
            filename = directory + player + '/' + testcasefile
            with open(filename) as json_file: 
                testcaseSet[player] = json.load(json_file)
            testcaseSet['isWithContext'] = testcaseSet[player]['isWithContext']
    else:
        filename = directory + testcasefile
        with open(filename) as json_file: 
            testcaseSet = json.load(json_file)
    return testcaseSet

def calculateEndpoint(testcase, point, targetpoint):
    if (targetpoint == None):
        return calculateEndpoint1(testcase, point)
    else:
        return calculateEndpoint2(testcase, point, targetpoint)

def calculateEndpointFirst(testcase, point):
    if (len(point) < 1):
        return []
    k = testcase["parameters"][1]

    sinx = testcase["sinx"]
    distance = testcase["distance"]

    # x and y mean the different value between two points
    # y / x = k    square(x) + square(y) = square(distance)
    y = -1
    if testcase["parameters"][0] == "first":
        y = numpy.sqrt(numpy.square(distance) /  (1/numpy.square(k) + 1) )
    
    #x = numpy.sqrt(numpy.square(distance) / (numpy.square(k) + 1) )
    if (sinx > 0 ):
        y = abs(y)
    else:
        y = -abs(y)
    x = y / k
    #print x, y
    return [max(point[0][0] + x, 0), max(point[0][1] + y, 0)]


def calculateEndpointSecond(testcase, point):
    if (len(point) < 2):
        return []
    # y = a * x **2 + b * x + c
    a = testcase["parameters"][1]
    # calculate b and c 
    x1 = point[0][0]
    y1 = point[0][1]
    x2 = point[1][0]
    y2 = point[1][1]
    d = testcase["distance"]

    denominator = x1 - x2 + 1E-08;
    numerator = (y1 - a * numpy.square(x1)) - (y2 - a * numpy.square(x2))
    b = numerator / denominator
    c = y1 - a * numpy.square(x1) - b * x1


    #print a, b , c
    x = Symbol('x')
    y = Symbol('y')
    solutions = solve([a * x * x + b * x + c - y, (x - x1) ** 2 + (y - y1) **2 - np.square(d) ], [x,y])
    
    endpoint = []
    for solution in solutions:
        if sympify(solution[0]).is_real:
            endpoint.append(solution)

    if (len(endpoint) == 0):
        return []

    sinx = testcase["sinx"]
    for p in endpoint:
        if (sinx > 0 ):
            if p[1] < y1:
                continue
            else:
                return [max(p[0], 0), max(p[1], 0)]
        else:
            if p[1] > y1:
                continue
            else:
                return [max(p[0], 0), max(p[1], 0)]
    return []


def getTypecCases(actiontype):
    while (True):
        index = random.randint(0, len(testcaseSet['case']) - 1)
        if testcaseSet['case'][index]["type"] == actiontype:
            return  testcaseSet['case'][index]

def getTestcases(num):
    cases = []
    if multiplayer == '1':
        player=screenObj.matchPlayer(imgpath, gamename, playerIcons, screencap)
        if player is None:
            return
        cases.append(testcaseSet[player]['case'][num])
        return cases

    if 'sequence' in testcaseSet and len(testcaseSet['sequence']) > 1:
        sequence = testcaseSet['sequence']
        for actiontype in sequence:
            cases.append(getTypecCases(actiontype))
        return cases

    else:
        cases.append(testcaseSet['case'][num])
        return cases
    
def getTestcasesContext(num):
    cases = []
    screencap = imgpath + gamename + '/screencap.png'
    context.map2array(screencap, playIcons, gamename)

    if 'sequence' in testcaseSet and len(testcaseSet['sequence']) > 1:
        sequence = testcaseSet['sequence']
        current_context = None
        actiontype = sequence[0]
        for case in testcaseSet['case']:
            if  case['type'] != actiontype:
                continue
            if current_context is None:
                point = context.contextmatch(screencap, playIcons, gamename, case['context'], case['contextX'], case["contextY"])
                if (point is not None ):
                    case["startX"] = point[0]
                    case["startY"] = point[1]
                    cases.append(case)
                    current_context = case['context']
                    #print cases
            else:
                if len(cases) < len(sequence):
                    if case['context'] != current_context:
                        continue
                    else:
                        point = context.pointmatch(screencap, playIcons, gamename, current_context, case['contextX'], case["contextY"])
                        if (point is not None ):
                            case["startX"] = point[0]
                            case["startY"] = point[1]
                            cases.append(case)
                else:                    
                    return cases

    else:
        for case in testcaseSet['case']:
            #print case
            point = context.contextmatch(screencap, playIcons, gamename, case['context'], case['contextX'], case["contextY"])
            if (point is not None ):
                #print point
                case["startX"] = point[0]
                case["startY"] = point[1]
                cases.append(case)
                return cases
    if len(cases) > 0:
        return cases
    else:
        if 'sequence' in testcaseSet and len(testcaseSet['sequence']) > 1:
            rand = random.randint(0, len(context.icons) - 1)
            points = context.arrays[context.icons[rand]]
            if points is None or len(points) < len(sequence):
                logger.error( "error , point should not be none or less")

            for i in range(len(sequence)):
                rand = random.randint(0, len(testcaseSet['case']) - 1)
                testcaseSet['case'][rand]["startX"] = points[i][0]
                testcaseSet['case'][rand]["startY"] = points[i][1]
                cases.append(copy.deepcopy(testcaseSet['case'][rand]))
                print ("No context matched, randomly pick two cases")
                #print cases
        else:
            rand = random.randint(0, len(context.icons) - 1)
            points = context.arrays[context.icons[rand]]
            rand = random.randint(0, len(points) - 1)
            startpoint = points[rand]
            rand = random.randint(0, len(testcaseSet['case'])-1)
            cases.append(testcaseSet['case'][rand])
            #print cases
            cases[0]["startX"] = startpoint[0] 
            cases[0]["startY"] = startpoint[1]
            print ("No context matched, randomly pick two cases")

        return cases
    return None

def play(num, cases):
    point = []
    if testcaseSet['isWithContext'] == 'Context':
        playIcons = cf.get(gamename, "playIcons")
        cf.remove_option(gamename, "playIcons")

    if cf.has_option(gamename, "playIcons"):
        playIcons = cf.get(gamename, "playIcons")
        startpoint = screenObj.matchPlayIcons(imgpath, gamename, playIcons, screencap)
    else:
        startpoint = (cases[0]["startX"], cases[0]["startY"])
    
    if testcaseSet['isWithContext'] == 'Context':
        cf.set(gamename, "playIcons", playIcons)

    point.append(startpoint)
    targetpoint = None
    if cf.has_option(gamename, "targetIcons"):
        targetIcon = cf.get(gamename, "targetIcons")
        targetpoint = screenObj.matchFunctionButton(imgpath, gamename, targetIcon, screencap,0.70)
        #print "target point : " + str(targetpoint)
        point.append(targetpoint)
        if targetpoint is None:
            logger.error ("no target found")
            return
        #Modified at July 7 2020  if the playicon is missing, we will use an alternative to continue generate testcases
        if (startpoint is None):
            startpoint = (cases[0]["startX"], cases[0]["startY"])
    if (startpoint is None):
        return


    testcases = cases
   
    for testcase in testcases:
        if testcase["type"] == "swipe":
            if (testcase["parameters"][0] == "first"):
                endPoint = calculateEndpointFirst(testcase, point)
            elif (testcase["parameters"][0] == "second"):
                endPoint = calculateEndpointSecond(testcase, point)
            if len(endPoint) == 2:
                #print endPoint
                adbkit.swipe(startpoint, endPoint, int(testcase["duration"] * 1000))

        if testcase["type"] == "tap":
            startpoint = (startpoint[0], startpoint[1])
            adbkit.click(startpoint)
        
    time.sleep(float(timeinterval))

if __name__ == '__main__':
    logger = Init()
    cf = getConfigure()
    cmdpath  = cf.get("system", "cmdpath")
    gamename = cf.get("system", "gameName")
    imgpath = cf.get("system", "imagepath")
    screencap = cf.get("system", "screencap")
    if cf.has_option(gamename, "playIcons"): 
        playIcons = cf.get(gamename, "playIcons")
    functionButton = cf.get(gamename, "functionButtonIcons")
    timeinterval = cf.get(gamename, "timeinterval")
    directory = cf.get(gamename, "dir")
    if cf.has_option(gamename, "playIcons"):
        playerIcons = cf.get(gamename, "playIcons")
    numberoftestcases = cf.get(gamename, "numberoftestcases")
    multiplayer = cf.get(gamename, "multiplayermode")

    logger.info("Test begins")
    device = cf.get("system", "device")
    adbkit = adb.adbKit(device)
    #adbkit.screenshots()
    testcaseSet = loadTestcase()

    screenObj = screen.ScreenOpe(testcaseSet["isWithContext"])
    context = contextarray.Context()

    if not adbkit.hasdevice():
        logger.error( "no device found")
        exit(1)
  
    time.sleep(5)
    
    for num in range(int(numberoftestcases)):
        while(True):
            screencap = adbkit.screenshots(gamename)
            try:
                point = screenObj.matchFunctionButton(imgpath, gamename, functionButton, screencap,0.80)
            except:
                continue
            if (point is not None):
                adbkit.click(point)
                time.sleep(1)
                continue
            else:
                if not cf.has_option(gamename, "playIcons"):
                    break
                startpoint = screenObj.matchPlayIcons(imgpath, gamename, playIcons, screencap)
                if (startpoint is not None):
                    break

                
        if testcaseSet["isWithContext"] == "Context":
            #screencap = adbkit.screenshots(gamename)
            cases = getTestcasesContext(num)
        else:
            cases = getTestcases(num)
        #print cases
        if cases is None:
            continue
        play(num, cases)


         


