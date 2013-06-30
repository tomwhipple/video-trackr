#!/usr/bin/env python
"""
Examine videos & track objects
"""

import sys
import time
import argparse

import cv
import cv2

WIN_NAME = "trackr"

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
        
    width = int(video.get(cv.CV_CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv.CV_CAP_PROP_FRAME_HEIGHT))
    fps = video.get(cv.CV_CAP_PROP_FPS)
    
    print "opened {w}x{h} video @ {f}fps".format(w=width,h=height,f=fps)
    
    cv2.namedWindow(WIN_NAME)
    cv2.moveWindow(WIN_NAME, 0, 0)
    cv2.resizeWindow(WIN_NAME, width, height)
    
    frame_count = 0
    while video.grab():
        got_frame, frame = video.retrieve()
        if not got_frame:
            print "frame miss"
            continue
        
        frame_count += 1
        print "frame: {c}   \r".format(c=frame_count), 
        sys.stdout.flush()
        
        cv2.imshow(WIN_NAME, frame)
        # time.sleep(0.01)
        key = cv2.waitKey(int(1000.0/fps))
        if key == 27:
            return
        elif key >= 0:
            print "\nkey: {k}\n".format(k=key)
        
    print
    
    # cv2.waitKey()
    video.release()
    
if __name__ == '__main__':
    sys.exit(main())