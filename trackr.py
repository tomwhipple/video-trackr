#!/usr/bin/env python
"""
Examine videos & track objects
"""

import sys
import argparse

import cv
import cv2

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    
    parser = argparse.ArgumentParser(description="Track moving objects in a video stream")
    
    parser.add_argument("-f", "--file", help="use given file")
    
    args = parser.parse_args(argv)
    
    source = args.file
    
    if source is None:
        print "No video source given!"
        return
        
    video = cv2.VideoCapture()
    video.open(source)
    
    if not video.isOpened():
        print "Video not open"
        return
        
    width = video.get(cv.CV_CAP_PROP_FRAME_WIDTH)
    height = video.get(cv.CV_CAP_PROP_FRAME_HEIGHT)
    fps = video.get(cv.CV_CAP_PROP_FPS)
    
    print "opened {w}x{h} video @ {f} fps".format(w=width,h=height,f=fps)
    
    
if __name__ == '__main__':
    sys.exit(main())