#!/usr/bin/env python

"""screen """
__author__ = 'zhaoyan@vt.edu'

import configparser
import sys
import os
import cv2
import numpy as np
import logging
import random
sys.path.append('../')

class ScreenOpe(object):
    def __init__(self, context):
        self.isWithContext = context

    def getResolution(self):
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


    def getSize(self):
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

    @staticmethod
    def match(small_img, big_img, match_type = 'max_loc', threshold = 0.60):
        if (not os.path.exists(small_img) or not os.path.exists(big_img)):
            return ()
        target_img = cv2.imread(big_img)
        find_img   = cv2.imread(small_img)
        find_height, find_width, find_channel = find_img.shape[::]
        result = cv2.matchTemplate(target_img, find_img, cv2.TM_CCOEFF_NORMED)
        if match_type == 'max_loc':
            min_val,max_val,min_loc,max_loc = cv2.minMaxLoc(result)
            if (max_val < threshold):
                return ()
            pointUpLeft = max_loc
        elif match_type == 'random_loc' or 'all':
            loc = np.where( result >= threshold)
            pt = tuple(zip(*loc[::-1]))
            if (len(pt) < 1):
                logging.warning(small_img + ' is not found')
                return None, find_height, find_width
            pt = ScreenOpe.clean(pt, find_height, find_width)
            if match_type == 'all':
                points = []
                for p in pt:
                    points.append((p[0] + (find_width/2), p[1] + (find_height/2)))
                return points, find_height, find_width
            rand = random.randint(0, len(pt) - 1)
            #logger.debug('random int from 0 to ' + str(len(pt) - 1) + 'is ' + str(rand))
            pointUpLeft = pt[rand]


        pointLowRight = (pointUpLeft[0]+find_width, pointUpLeft[1]+find_height)
        pointCentre   = (pointUpLeft[0]+(find_width/2), pointUpLeft[1]+(find_height/2))

        return pointCentre
        

    @staticmethod
    def clean(pt, find_height, find_width):
        pt_clean = []
        pt_clean.append(pt[0])
        for (x, y) in pt[1:]:
            repeat = False
            for (p_x, p_y) in pt_clean:
                if (abs(x - p_x) < find_width/2  and abs(y-p_y) < find_height/2):
                    repeat = True
                    break
            if repeat:
                continue
            else:
                pt_clean.append((x, y))
        return pt_clean
    @staticmethod
    def matchNumber(small_img, big_img):
        if (not os.path.exists(small_img) or not os.path.exists(big_img)):
            return 0

        point, height, width = ScreenOpe.match(small_img, big_img, 'all', 0.90)
        if (point is None):
            logging.warning(small_img + ' is not found')
            return 0

        return len(point)


    def matchFunctionButton(self, imgpath, gamename, buttonlist, screencap,score= 0.85):
        buttons = buttonlist.split(',')
        for button in buttons:
            buttonimg = imgpath+gamename+'/'+button
            point = self.match(buttonimg, screencap, 'max_loc', score)
            if len(point) == 2:
                print(buttonimg)
                return point

    def matchPlayIcons(self, imgpath, gamename, elementList, screencap):
        #elementList = cf.get(gamename, 'playElements')
        elements = elementList.split(',')
        if (self.isWithContext == "multiple"):
            print("random pick")
            Icons = self.matchedPlayIcons(imgpath, gamename, elementList, screencap)
            rand = random.randint(0, len(Icons) - 1)
            point = self.match(Icons[rand], screencap, 'random_loc')
            if point:
                return point
            else:
                return None

        for element in elements:
            elementimg = imgpath+gamename+'/'+element
            point = self.match(elementimg, screencap)
            if point:
                return point

    def matchMultiplePlayIcons(self, imgpath, gamename, elementList, screencap, count):
        elements = elementList.split(',')
        Icons = self.matchedPlayIcons(imgpath, gamename, elementList, screencap)
        rand = random.randint(0, len(Icons) - 1)
        point, height, width = self.match(Icons[rand], screencap, 'all', 0.90)
        if point is None:
            return None
        else:
            return point[0:count]
            

    def matchPlayer(self, imgpath, gamename, elementList, screencap):
        elements = elementList.split(',')
        for element in elements:
            elementimg = imgpath+gamename+'/'+element
            point = self.match(elementimg, screencap)
            if point:
                return element
        return None
    @staticmethod
    def static_numberOfPlayIcons(imgpath, gamename, elementList, screencap):
        elements = elementList.split(',')
        count = 0
        for element in elements:
            elementimg = imgpath+gamename+'/'+element
            count += ScreenOpe.matchNumber(elementimg, screencap)

        return count

    def matchedPlayIcons(self, imgpath, gamename, elementList, screencap):
        elements = elementList.split(',')
        matchedIcons = []
        for element in elements:
            elementimg = imgpath+gamename+'/'+element
            count = self.matchNumber(elementimg, screencap)
            if count > 0:
                matchedIcons.append(elementimg)

        return matchedIcons
