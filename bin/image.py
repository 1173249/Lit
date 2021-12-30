#!/usr/bin/env python
#coding=utf-8

import cv2 as cv

img = cv.imread("candy.png")
cv.namedWindow("Image")
cv.imshow("Image", img)
cv.waitKey(0)
cv.destroyAllWindows()
