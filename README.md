Trackr
======

Experiments in video object tracking. 

**This is a very preliminary project.**

Prerequisites
-------------

1. (Homebrew)[http://mxcl.github.io/homebrew/]
2. (ffmpeg)[http://ffmpeg.org/]  via `brew install ffmpeg`
3. (OpenCV)[http://opencv.org/]  from source `git clone https://github.com/Itseez/opencv.git`. Building from scratch is probably not be strictly necessary, but we need video & Python suppport. Source install anticipates future hacking. ;)
4. A Python virtualenv is recommended.

Setup
-----

1. Ensure opencv is in your PYTHONPATH.  (example)[https://github.com/tomwhipple/profile/blob/master/bash_profile]
2. If `$ ./trackr.py -h` doesn't generate errors, we're good to go. Otherwise install missing modules via pip.

Running
-------

It's best to work with downsampeled videos for development. 426x240 seems reasonable. ffmpeg can be used to resize the video.

Start by just playing a video: `$ ./trackr.py -p -f videos/circles_240.avi`