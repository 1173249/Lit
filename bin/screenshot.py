#!/usr/bin/env python
# coding=utf-8

adb_path='/home/adminadmin/Android/Sdk/platform-tools'
logfile='command.log'
import commands
import sys, time
import cv2
import numpy as np
import logging
import random
from adblibs import adb
from time import gmtime, strftime


if __name__ == '__main__':
    adbkit = adb.adbKit()
    for i in range (0,500):
        serialnum = strftime(".%H%M%S", gmtime())
        adbkit.screenshots(serialnum)

