#!/usr/bin/env python

import sys
sys.path.append('../')
from adblibs import adb
from screenlibs import screen
import contextlibs
from contextlibs import contextarray
import configparser
import os
import logging
import json
import numpy
import codecs
import logging
from scipy import optimize
import numpy as np



def withContext():
    gamename = cf.get("system", "gameName")
    imgpath = cf.get("system", "imagepath")
    screencap = cf.get("system", "screencap")
    number = 0

    if cf.has_option(gamename, "targetIcons"):
        return "Target"
    if cf.has_option(gamename, "playIcons"): 
        playIcons = cf.get(gamename, "playIcons")
        number = screen.ScreenOpe.static_numberOfPlayIcons(imgpath, gamename, playIcons, screencap)
    if cf.has_option(gamename, "targetIcons"):
        targetIcons = cf.get(gamename, "targetIcons")
    else:
        targetIcons = ""
    
    if (number <= 1 and len(targetIcons) < 1):
        return "None"
    elif (number <= 1 and len(targetIcons) > 0):
        return "Target"
    if (number > 1):
        return "Context"

def Init():
    formatter_str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    log_level = logging.DEBUG
    logging.basicConfig(filename=logfile, format=formatter_str, level=log_level)
    logger = logging.getLogger(__name__)
    return logger


def getConfigure():
    root_dir = os.path.dirname(os.path.abspath('.'))
    cf = configparser.ConfigParser()
    cf.read(root_dir+"/conf/config.ini")
    secs = cf.sections()
    return cf

def f_1(x, A, B):    
    return A*x + B 
    
def f_2(x, A, B, C):
    return A*x*x + B*x + C

def first_order_function_fitting(x, y):
    A1, B1 = optimize.curve_fit(f_1, x, y)[0]
    return A1, B1

def second_order_function_fitting(x, y):
    A2, B2, C2= optimize.curve_fit(f_2, x, y)[0]
    return A2, B2, C2

def mean_square_error1(x, y, A1, B1):
    sum = 0
    for i in range(0, len(x)):
        eachy = f_1(x[i], A1, B1)
        sum += np.square( eachy - y[i] )
    return sum

def mean_square_error2(x, y, A2, B2, C2):
    sum = 0
    for i in range(0, len(x)):
        eachy = f_2(x[i], A2, B2, C2)
        sum += np.square( eachy - y[i])
    return sum

def function_fitting(x, y):
    error2 = sys.maxsize
    A1, B1 = first_order_function_fitting(x, y)
    if (len(x) > 2):
        A2, B2, C2 = second_order_function_fitting(x, y)
        error2 = mean_square_error2(x, y, A2, B2, C2)
        print("A2=" +str(A2))
    error1 = mean_square_error1(x, y, A1, B1)
    #print "error1 = " + str(error1)
    #print "error2 = " + str(error2)
    if (error1 <= error2):
        return "first", A1, B1
    else:
        return "second", A2, B2, C2


def swipeAction(eachA):
    distance = numpy.sqrt(
            numpy.square(eachA["endY"] - eachA["startY"])
            + numpy.square(eachA["endX"] - eachA["startX"])
            )
    
    x = [eachA["startX"], eachA["endX"]]
    y = [eachA["startY"], eachA["endY"]]
    #k, b = first_order_function_fitting(x, y)
    parameters = function_fitting(x, y)
    sinx = (eachA["endY"] - eachA["startY"])/ distance
    return distance, sinx, parameters

def swipeActionT(eachA, point):
    distance, sinx, parameters = swipeAction(eachA)
    x = [eachA["endX"], eachA["startX"], point[0]]
    y = [eachA["endY"], eachA["startY"], point[1]]
    #if abs(x[0] - x[-1]) < abs(y[0] - y[1]):
    #    parameters = function_fitting(y, x)
    #    t1 = list(parameters)
    #    t1.append('r')
    #    parameters = tuple(t1)
    #else:
    print (x)
    print (y)
    parameters = function_fitting(x, y)
    return distance, sinx, parameters

def deviation(point, parameters):
    Denominator = numpy.sqrt(numpy.square(point[0]) + numpy.square(point[1]))
    numerator = parameters[1] * point[0] + parameters[2] - point[1]
    deviation = abs(numerator / Denominator)
    return deviation

def functionAnalyze(filepath):
    gamename = cf.get("system", "gameName")
    functionfile = filepath + cf.get(gamename, "functionfile")
    with open(functionfile) as json_file:
        actionSet = json.load(json_file)
        module["sequence"] = actionSet["sequence"]

def actionAnalyze(filepath):
    gamename = cf.get("system", "gameName")
    actionfile = filepath + cf.get(gamename, "actionfile")
    with open(actionfile) as json_file:
        actionSet = json.load(json_file)
        for eachAction in actionSet["actions"]:
            if eachAction["type"] == "swipe":
                distance, sinx, parameters = swipeAction(eachAction)
                module["paradigm"].append({"type":"swipe", 
                        "distance":distance, "parameters":parameters, 
                        "sinx":sinx, "duration":eachAction["duration"],
                        "startX": eachAction["startX"], "startY": eachAction["startY"]})
            if eachAction["type"] == "tap":
                module["paradigm"].append({"type":"tap","startX": eachAction["startX"],
                    "startY": eachAction["startY"], "duration":eachAction["duration"]})
         
        module["sequence"] = actionSet["sequence"]

def actionTargetAnalyze(filepath):
    gamename = cf.get("system", "gameName")
    actionfile = filepath + cf.get(gamename, "actionfile")
    with open(actionfile) as json_file:
        actionSet = json.load(json_file)
        for eachAction in actionSet["actions"]:
            img = imgpath+gamename+"/screencap.png." + eachAction["timestamp"]
            print(img)
            point = screen.matchFunctionButton(imgpath, gamename, targetIcon, img)
            if (point is None):
                print ("find no target")
                continue
            else:
                print (point)

            if eachAction["type"] == "swipe":
                distance, sinx, parameters = swipeActionT(eachAction, point)
                #targetDeviation = deviation(point, parameters)
                module["paradigm"].append({"type":"swipe", 
                        "distance":distance, "parameters":parameters, 
                        "sinx":sinx, "duration":eachAction["duration"]})
            if eachAction["type"] == "tap":
                module["paradigm"].append({"type":"tap", "duration":eachAction["duration"]})
        module["sequence"] = actionSet["sequence"]


def contextAnalyze():
    logger.info("context analyze")
    gamename = cf.get("system", "gameName")
    playIcons =  cf.get(gamename, "playIcons")

    actionfile = filepath + cf.get(gamename, "actionfile")
    with open(actionfile) as json_file:
        actionSet = json.load(json_file)
        for eachAction in actionSet["actions"]:
            img = imgpath+gamename+"/screencap.png." + eachAction["timestamp"]
            print (eachAction["timestamp"])
            iconarray, y, x = context.searchInArray(img, playIcons, gamename, eachAction)  
            if eachAction["type"] == "swipe":
                 distance, sinx, parameters = swipeAction(eachAction)
                 module["paradigm"].append({"type":"swipe",
                        "distance":distance, "parameters":parameters,
                        "sinx":sinx, "duration":eachAction["duration"],
                        "context":iconarray, "contextY":y, "contextX":x,
                        "timestamp": eachAction["timestamp"]})
            if eachAction["type"] == "tap":
                module["paradigm"].append({"type":"tap",
                     "duration":eachAction["duration"],
                     "context":iconarray, "contextY":y, "contextX":x,
                     "timestamp": eachAction["timestamp"]})
    module["sequence"] = actionSet["sequence"]

def dump2File(outfilename, module):
    if ( not module):
        return
    out = codecs.open(outfilename, 'w', 'utf8')
    out.write(json.dumps(module, indent = 4, sort_keys=True, ensure_ascii=False))
    out.close()

if __name__ == '__main__':
    cf = getConfigure()
    logfile = cf.get("system", "logfile")
    logger = Init()

    screepcapImage = cf.get("system", "screencap")
    imgpath = cf.get("system", "imagepath")
    gamename = cf.get("system", "gameName") 
    if cf.has_option(gamename, "targetIcons"):
        targetIcon = cf.get(gamename, "targetIcons")
    
    #screen = screen.ScreenOpe("None")
    if cf.has_option(gamename, "isWithContext"):
        iswithContext =  cf.get(gamename, "isWithContext")
    else:
        iswithContext = withContext()

    if (iswithContext == "None"):
        logger.info("not with Context")
    else:
        logger.info("with Context" + iswithContext)

    screen = screen.ScreenOpe(iswithContext)
    iswithPlayIcon = cf.has_option(gamename, "playIcons")
    if (not iswithPlayIcon):
        logger.info("not with play icon")

    directory = cf.get(gamename, "dir")
    multiplayer = cf.get(gamename, "multiplayermode")
    context = contextarray.Context()

    
    if multiplayer == '1':
        playerIcons = cf.get(gamename, "playIcons")
        players = playerIcons.split(',')
        for player in players:
            module = {}
            module["paradigm"] = []
            filepath = directory + player + '/'
            if (iswithContext == "None"):
                actionAnalyze(filepath)
            elif (iswithContext == "Target"):
                actionTargetAnalyze(filepath)
            else:
                contextAnalyze()

            module["isWithContext"] = iswithContext
            modulefile =  directory + player + '/' + cf.get(gamename, "modulefile")
            dump2File(modulefile, module)
    else:
        module = {}
        module["paradigm"] = []
        filepath = directory
        if (iswithContext == "None" or iswithContext == "multiple"):
            actionAnalyze(filepath)
        elif (iswithContext == "Target"):
            actionTargetAnalyze(filepath)
        else:
            contextAnalyze()
        module["isWithContext"] = iswithContext
        modulefile =  directory + cf.get(gamename, "modulefile")
        dump2File(modulefile, module)
        module = {}
        #modulefile =  directory + cf.get(gamename, "function_modulefile")
        #functionAnalyze(filepath)
        #dump2File(modulefile, module)

