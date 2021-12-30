#!/usr/bin/env python

import copy
import sys
sys.path.append('../')

from screenlibs import screen
from interval import Interval
from collections import deque 
import cv2
import random
"""array"""

class Context(object):
    def map2array(self, target_img, playIcons, gamename):
        self.max_x = 0;
        self.min_x = 1040;
        self.max_y = 0;
        self.min_y = 2560;
        candy_pt = {}
        icons = playIcons.split(',')
        self.arrays = {}
        self.icons = [] 
        for icon in icons:
            img_name = '../image/'+gamename+'/' + icon
            pt, self.find_height, self.find_width = screen.ScreenOpe.match(img_name, target_img, 'all', 0.91)
            if pt is None:
                continue
            print("There are " + str(len(pt)) + " for " + icon)
            self.arrays[icon] = copy.deepcopy(pt)
            self.icons.append(icon)
            for p in pt:
                self.max_x = max(self.max_x, p[0])
                self.min_x = min(self.min_x, p[0])
                self.max_y = max(self.max_y, p[1])
                self.min_y = min(self.min_y, p[1])
            del pt[:]
        #for debug
        return self.arrays

    def identifyIcons(self, playIcons, action):
        icons = playIcons.split(',')
        endicon = None
        for icon in icons:
            if icon not in self.arrays:
                continue
            for p in self.arrays[icon]:
                if int(action['startX']) in Interval(p[0] - self.find_width / 2, p[0] + self.find_width / 2) \
                        and action['startY'] in Interval(p[1] - self.find_height / 2, p[1] + self.find_height / 2):
                    starticon = icon
                if 'endX' not in action:
                    continue
                if action['endX'] in Interval(p[0], p[0] + self.find_width) \
                        and action['endY'] in Interval(p[1], p[1] + self.find_height):
                    endicon = icon

        return starticon, endicon

    def contextmatch(self, img, playIcons, gamename, context, startX, startY):
        icons = playIcons.split(',')
        #arrays = self.map2array(img, playIcons, gamename)

        axis_x = int((self.max_x - self.min_x) * 1.0 / self.find_width + 1.5)
        axis_y = int((self.max_y - self.min_y) * 1.0 / self.find_height + 1.5)

        self.bg_array = [['-1'] * axis_x for row in range(axis_y)]
        self.fill2backgroundarray(self.arrays, self.min_x, self.min_y, self.find_width, self.find_height)
        random.shuffle(icons)
        for icon in icons:
            if icon not in self.arrays:
                continue
            self.screen_array = copy.deepcopy(self.bg_array)
            self.fill2array(self.arrays[icon], self.min_x, self.min_y, self.find_width, self.find_height)
            print(icon)
            print(self.screen_array)
            matchpoint = self.array_in_screen(context, startX, startY)
            if matchpoint is not None:
                self.icon = icon
                return matchpoint

        return None

    def pointmatch(self, img, playIcons, gamename, context, startX, startY):
        axis_x = int((self.max_x - self.min_x) * 1.0 / self.find_width + 1.5)
        axis_y = int((self.max_y - self.min_y) * 1.0 / self.find_height + 1.5)
        #print self.icon
        self.fill2array(self.arrays[self.icon], self.min_x, self.min_y, self.find_width, self.find_height)
        matchpoint = self.array_in_screen(context, startX, startY)
        if matchpoint is not None:
            return matchpoint

        return matchpoint


    #match coordiantes to piexel coordinates
    def match2pixels(self, matchpoint, startX, startY):
        x = self.min_x + self.find_width * (matchpoint[1] + startX )
        y = self.min_y + self.find_height * (matchpoint[0] + startY )
        #print "match2pixels", x, y
        return [x, y]

    def matchIcons(self, icon, number):
        m, n = self.arrays[icon].shape
        #print m, n

    #find the pattern based on the action and context
    def searchInArray(self, target_img, playIcons, gamename, action):
        self.map2array(target_img, playIcons, gamename)
        starticon, endicon = self.identifyIcons(playIcons, action)
        axis_x = (self.max_x - self.min_x) / self.find_width + 1
        axis_y = (self.max_y - self.min_y) / self.find_height + 1
        #print starticon

        self.screen_array = [['0'] * int(axis_x) for row in range(int(axis_y))]
        self.screen_array = self.fill2array(self.arrays[starticon], self.min_x, self.min_y, self.find_width, self.find_height)
        #print self.screen_array
        startX = int((action['startX'] - self.min_x) * 1.0 / self.find_width + 0.25)
        startY = int((action['startY'] - self.min_y) * 1.0 / self.find_height + 0.25)
        if action["type"] == "swipe":
            endX =  int((action['endX'] - self.min_x) * 1.0/ self.find_width + 0.5)
            endY = int((action['endY'] - self.min_y) * 1.0/ self.find_height + 0.5)
        #print startX, startY
        #print self.screen_array
        search_array = self.search_array(self.screen_array, startX, startY)
        if action["type"] == "swipe":
            temp_array = self.search_array(self.screen_array, endX, endY)
            for p in temp_array:
                search_array.append(p)
        #print self.screen_array

        pattern = self.formPattern(search_array,startX, startY)
        #print self.screen_array
        return pattern

    #from pixel array to index array
    def fill2array(self, array, min_x, min_y, find_width, find_height):
        for coordinate in array:
            axis_x = int((coordinate[0] - min_x) * 1.0 / find_width + 0.5)
            axis_y = int((coordinate[1] - min_y) * 1.0 / find_height + 0.5)
            self.screen_array[axis_y][axis_x] = '1'
        #print screen_array
        return self.screen_array
    def fill2backgroundarray(self, arrays, min_x, min_y, find_width, find_height):
        for icon in arrays:
            for coordinate in arrays[icon]:
                axis_x = int((coordinate[0] - min_x) * 1.0 / find_width + 0.5)
                axis_y = int((coordinate[1] - min_y) * 1.0 / find_height + 0.5)
                self.bg_array[axis_y][axis_x] = '0'
        return self.bg_array

    #find the pattern
    def formPattern(self, search_array, startX, startY):
        max_x = 0;
        min_x = 1000;
        max_y = 0;
        min_y = 1000;
        for p in search_array:
            max_x = max(max_x, p[0])
            min_x = min(min_x, p[0])
            max_y = max(max_y, p[1])
            min_y = min(min_y, p[1])

        axis_x = (max_x - min_x) + 1
        axis_y = (max_y - min_y) + 1
        result = [['0'] * axis_x for row in range(axis_y)]
        #print result
        for p in search_array:
            #print p[0] - min_x
            #print p[1] - min_y
            result[p[1] - min_y][p[0] - min_x] = '1'
        #print result
        #print startX-min_x, startY-min_y
        return result, startY-min_y, startX-min_x

    def search_array(self, array, x, y):
        result=[]
        width = len(array[0])
        height = len(array)
        q = deque()
        q.append([x,y])
        while (q):
            point = q.popleft()
            if array[point[1]][point[0]] == '1':
                result.append(point)
                array[point[1]][point[0]] = '0'
            if point[0]+1 < width and array[point[1]][point[0]+1] == '1':
                q.append([point[0]+1,point[1]])
            if point[0]-1 >= 0 and array[point[1]][point[0]-1] == '1':
                q.append([point[0]-1,point[1]])
            if point[1]+1 < height and array[point[1]+1][point[0]] == '1':
                q.append([point[0],point[1]+1])
            if point[1]-1 >= 0 and array[point[1]-1][point[0]] == '1':
                q.append([point[0],point[1]-1])
            #print q
        return result

    def array_in_screen(self, small, x, y):
        big = self.screen_array
        return self.array_in(small, big, x, y)

    def array_in(self, small, big, x, y):
        #print small
        #print big
        m = len(big)
        n = len(big[0])
        for i in range(m - len(small) + 1):
            for j in range(n - len(small[0]) + 1):
                if small[0] == big[i][j: j+len(small[0])]:
                    for k in range(len(small)):
                        if small[k] == big[i+k][j: j+len(small[k])]:
                            pass
                        else:
                            break
                    if k == (len(small)-1) and small[k] == big[i+k][j: j+len(small[k])]:
                        #print "array_in", i, j, x, y
                        return self.match2pixels([i, j], x, y)

                else:
                    continue
        return None

if __name__ == "__main__":
    context = Context()
    #pt, find_height, find_width =
    action = {"duration": 0.5272720000066329,"startX": 108,"startY": 330,"endX": 85,"endY": 467,"timestamp": "1581449161.64","type": "swipe"}

    small = context.searchInArray('/home/adminadmin/Desktop/Lab/image/candycrush/screencap.png.1581449161.64', 'yellow.png,red.png,blue.png,green.png,purple.png,orange.png', 'candycrush', action)
     
    print (context.contextmatch('/home/adminadmin/Desktop/Lab/image/candycrush/screencap.png.1581449161.64', 'yellow.png,red.png,blue.png,green.png,purple.png,orange.png', 'candycrush', small[0], 1, 1) )
