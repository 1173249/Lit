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
import random
import codecs

def getConfigure():
    root_dir = os.path.dirname(os.path.abspath('.'))
    print (root_dir)
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


def genRange4Swipe(paradigms):
    swipeRange = {}
    for para in paradigms:
        if para["type"] != 'swipe':
            continue
        for key in para:
            if key in swipeRange:
                swipeRange[key].append(para[key])
            else:
                swipeRange[key] = [para[key]]
    return swipeRange

def genRange4Tap(paradigms):
    swipeRange = {}
    for para in paradigms:
        if para["type"] != 'tap':
            continue
        for key in para:
            if key in swipeRange:
                swipeRange[key].append(para[key])
            else:
                swipeRange[key] = [para[key]]
    return swipeRange

"""def genRange4Swipe(paradigms):
    Angle = paradigms[0]["angle"]
    minAngle = paradigms[0]["angle"]

    maxDis = paradigms[0]["distance"]
    minDis = paradigms[0]["distance"]

    maxDuration = paradigms[0]["duration"]
    minDuration = paradigms[0]["duration"]

    for para in paradigms:
        maxAngle = max(para["angle"], maxAngle)
        minAngle = min(para["angle"], minAngle)
        maxDis = max(para["distance"], maxDis)
        minDis = min(para["distance"], maxDis)
        maxDuration = max(para["duration"], maxDuration)
        minDuration = min(para["duration"], minDuration)

    swipeRange = {}
    swipeRange["maxAngle"] = maxAngle
    swipeRange["minAngle"] = minAngle
    swipeRange["maxDis"] = maxDis
    swipeRange["minDis"] = minDis
    swipeRange["maxDuration"] = maxDuration
    swipeRange["minDuration"] = minDuration

    return swipeRange
"""

def genCase4Swipe(paradigms):
    caseAction = {}
    if typeoftestcases == '1':
        swipeRange = genRange4Swipe(paradigms)
        for key in swipeRange:
            value = swipeRange[key][random.randint(0, len(swipeRange[key]) - 1)]
            caseAction[key] = value

    return caseAction


def genCase4Tap(paradigms):
    caseAction = {}
    if typeoftestcases == '1':
        swipeRange = genRange4Tap(paradigms)
        for key in swipeRange:
            value = swipeRange[key][random.randint(0, len(swipeRange[key]) - 1)]
            caseAction[key] = value
    return caseAction

def genCase4SwipeTarget(paradimgs):
    return {} 

def genCaseWithoutContext(paradigms):
    if paradigms is None:
        return 
    numberOfCase = cf.get(gamename, "numberoftestcases")
    testcases = {}
    testcases["case"] = []
    numOfPara = len(paradigms)

    for i in range(0, int(numberOfCase)):
        if paradigms[i%numOfPara]["type"] ==  "swipe":
            testcases["case"].append(genCase4Swipe(paradigms) )
        if paradigms[i%numOfPara]["type"] == "tap":
            testcases["case"].append(genCase4Tap(paradigms))

    
    return testcases


def genCaseWithTarget(paradigms):
    if paradigms is None:
        return
    numberOfCase = cf.get(gamename, "numberoftestcases")
    testcases = {}
    testcases["case"] = []
    numOfPara = len(paradigms)

    for i in range(0, int(numberOfCase)):
        if paradigms[i%numOfPara]["type"] == "swipe":
            testcases["case"].append(genCase4Swipe(paradigms) )
        if paradigms[i%numOfPara]["type"] == "tap":
            testcases["case"].append(genCase4Tap(paradigms) )

    return testcases


def genCaseWithContext(paradigms):
    if paradigms is None:
        return
    testcases = {}
    testcases["case"] = paradigms
    return testcases


def loadModule(player=''):
    modulefile = directory + player + '/' + cf.get(gamename, "modulefile")
    with open(modulefile) as json_file:
        module = json.load(json_file)
    return module

def dump2File(outfilename, module):
    if ( not module):
        return
    out = codecs.open(outfilename, 'w', 'utf8')
    out.write(json.dumps(module, indent = 4, sort_keys=True, ensure_ascii=False))
    out.close()


if __name__ == '__main__':
    logger = Init()
    cf = getConfigure()
    cmdpath  = cf.get("system", "cmdpath")
    gamename = cf.get("system", "gameName")
    imgpath = cf.get("system", "imagepath")
    screencap = cf.get("system", "screencap")
    logger.info("Game begins")
    device = cf.get('system', "device")
    adbkit = adb.adbKit(device)
    directory = cf.get(gamename, "dir")


    typeoftestcases = cf.get(gamename, "typeoftestcases")
    multiplayer = cf.get(gamename, "multiplayermode")

    if multiplayer == '1':
        playerIcons = cf.get(gamename, "playIcons")
        players = playerIcons.split(',')
        for player in players:
            module = loadModule(player)
            testcases = {}
            if module["isWithContext"] == "None":
                testcases = genCaseWithoutContext(module["paradigm"])
            elif module["isWithContext"] == "Target":
                testcases = genCaseWithTarget(module["paradigm"])

            outfilename = directory + player + '/' + cf.get(gamename, "testcasefile")
            dump2File(outfilename, testcases)

    else:
        module = loadModule()
        testcases = {}
        if module["isWithContext"] == "None" or module["isWithContext"] == "multiple":
            testcases = genCaseWithoutContext(module["paradigm"])
        elif module["isWithContext"] == "Target":
            testcases = genCaseWithTarget(module["paradigm"])
        elif module["isWithContext"] == "Context":
            testcases = genCaseWithContext(module["paradigm"])

        if "sequence" in module:
            testcases["sequence"] = module["sequence"]
        testcases["isWithContext"] = module["isWithContext"]
        outfilename = directory + cf.get(gamename, "testcasefile")
        dump2File(outfilename, testcases)
    #for testcase in testcases["case"]:
    #    print testcase

    


         


