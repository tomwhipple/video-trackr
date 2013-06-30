#!/usr/bin/env python

import cv
import sys

files = sys.argv[1:]

for f in files:
    capture = cv.CaptureFromFile(f)
    print capture

    print cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH)
    print cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT)

    for i in xrange(10000):
        frame = cv.QueryFrame(capture)
        if frame:
            print frame