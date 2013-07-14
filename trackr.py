#!/usr/bin/env python
"""
Examine videos & track objects
"""

import sys
import time
import argparse

import cv
import cv2
import numpy as np

WIN_NAME = "trackr"

# TODO: wtf do these do, exactly? Well, let's start with the example values from motempl.py
# http://docs.opencv.org/modules/video/doc/motion_analysis_and_object_tracking.html#calcmotiongradient
MAX_TIME_DELTA = 0.25
MIN_TIME_DELTA = 0.05

def make_nth_named_window(name, height, n=0, x=0):
    cv2.namedWindow(name)
    y = n * height
    cv2.moveWindow(name, x, y)

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    
    parser = argparse.ArgumentParser(description="Track moving objects in a video stream")
    
    parser.add_argument("-f", "--file", 
                        help="use given file")
    parser.add_argument("-p", "--play-only", action="store_true",
                        help="playback only. Don't do any recognition. Useful for sanity checking files or installation")
    parser.add_argument("--motion-threshold", type=int, default=32,
                        help="threshold for motion. (difference in grey values between frames)")
    parser.add_argument("--max-track-time", type=float, default=0.5,
                        help="maximum time for a motion track")
    
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
    
    HISTORY_NAME = "motion history"
    MASK_NAME = "motion mask"
    ORIENTATION_NAME = "orientation"
    
    make_nth_named_window(WIN_NAME, height)
    
    if not args.play_only:
        make_nth_named_window(HISTORY_NAME, height, 1)
        # make_nth_named_window(MASK_NAME, height, 2)
        # make_nth_named_window(ORIENTATION_NAME, height, 3)
        
        motion_history = np.zeros((height, width), np.float32)
        
    prev_frame = None
    
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
        
        timestamp = float(frame_count) / fps
        
        if not args.play_only:
            if prev_frame is None:
                prev_frame = frame.copy()
                
            frame_diff = cv2.absdiff(frame, prev_frame)
            gray_diff = cv2.cvtColor(frame_diff, cv2.COLOR_BGR2GRAY)
            ret, motion_mask = cv2.threshold(gray_diff, args.motion_threshold, 1, cv2.THRESH_BINARY)
            # cv2.imshow(MASK_NAME, motion_mask)
            
            cv2.updateMotionHistory(motion_mask, motion_history, timestamp, args.max_track_time)
            cv2.imshow(HISTORY_NAME, motion_history)
            
            mgrad_mask, mgrad_orient = cv2.calcMotionGradient( motion_history, MAX_TIME_DELTA, MIN_TIME_DELTA, apertureSize=5 )
            mseg_mask, mseg_bounds = cv2.segmentMotion(motion_history, timestamp, MAX_TIME_DELTA)
            
            # cv2.imshow(ORIENTATION_NAME, mgrad_orient)
            
            prev_frame = frame
        
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