#!/usr/bin/env python

import sys
sys.path.append('../')
from adblibs import adb
from screenlibs import screen
import ConfigParser
import os
import logging
import time
from multiprocessing import Process
import shutil
import signal
import subprocess

def Init():
    formatter_str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    log_level = logging.DEBUG
    logging.basicConfig(filename=logfile, format=formatter_str, level=log_level)
    logger = logging.getLogger(__name__)
    return logger

def getConfigure():
    root_dir = os.path.dirname(os.path.abspath('.'))
    print (root_dir)
    cf = ConfigParser.ConfigParser()
    cf.read(root_dir+"/conf/config.ini")
    secs = cf.sections()
    return cf

def clean(gamename, imgpath, directory):
    cmd = 'rm ' + imgpath + gamename + '/' + 'screencap.png.*'
    os.system(cmd)
    cmd = 'rm -r ' + directory
    os.system(cmd)
    cmd = 'mkdir ' + directory
    os.system(cmd)
    if multiplayer == '1':
        players = playerIcons.split(',')
        for player in players:
            cmd = 'mkdir -p ' +  directory + player + '/trace'
            os.system(cmd)
    else:
        cmd = 'mkdir -p ' +  directory + 'trace'
        os.system(cmd)

def writetime2tracefile(tracefile):
    with open (tracefile, "w+") as pf:
        ticks = time.time()
        pf.write(str(ticks)+'\n')



if __name__ == '__main__':
    cf = getConfigure()
    logfile = cf.get("system", "logfile")
    logger = Init()
    cmdpath  = cf.get("system", "cmdpath")
    gamename = cf.get("system", "gameName")
    device = cf.get("system", "device")
    adbkit = adb.adbKit(device)
    screen = screen.ScreenOpe("None")
    buttonlist = cf.get(gamename, 'functionButtonIcons')
    imgpath = cf.get("system", "imagepath")
    screencap = cf.get("system", "screencap")
    tracefile = cf.get(gamename, "tracefile")
    diretory = cf.get(gamename, "dir")
    multiplayer = cf.get(gamename, "multiplayermode")
    playerIcons = cf.get(gamename, "playIcons")
    directory = cf.get(gamename, "dir")
    clean(gamename, imgpath, directory)
    writetime2tracefile(tracefile)
    

    print os.getpid() 
    while (True):
        ticks = time.time()
        screenname = adbkit.screenshots(gamename, str(ticks))
        shutil.copy(screenname ,screencap)
        try:
            point = screen.matchFunctionButton(imgpath, gamename, buttonlist, screencap)
        except:
            continue
        if (point is not None):
            adbkit.click(point)
            print("click a function button")
            continue
        

        if multiplayer == '1':
            player=screen.matchPlayer(imgpath, gamename, playerIcons, screencap)
            if player is None:
                continue
            print "please play next step"
            p1 = Process(target = adbkit.getevent, args=(diretory+str(player)+'/trace/'+tracefile+'.'+str(ticks), return_dict) )
        else:
            if not cf.has_option(gamename, "playIcons"):
                print "please play next step"
                adbkit.getevent(diretory+'/trace/'+tracefile+'.'+str(ticks))
            else:
                playIcons = cf.get(gamename, "playIcons")
                startpoint = screen.matchPlayIcons(imgpath, gamename, playIcons, screencap)
                if (startpoint is None):
                    continue
                else:
                    print "please play next step"
                    adbkit.getevent(diretory+'/trace/'+tracefile+'.'+str(ticks))


            #p1 = Process(target = adbkit.getevent, args=(diretory+'/trace/'+tracefile+'.'+str(ticks), return_dict) )
        #p1.start()
        #time.sleep(9)
        #p1.terminate()
        #p1.join()
        #print p1, p1.is_alive()



            
        
