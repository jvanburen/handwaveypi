#!/usr/bin/env python3
from collections import namedtuple
HUD = namedtuple("HUD", ('image', 'blob1', 'blob2', 'time'))
##class HUD:
##    def __init__(self, image, blob1, blob2, time):
##        self.image = image #pygame surface of the image to display
##        self.lblob = blob1 # coordinates in [0, 1]^2 of the first blob
##        self.blob2 = blob2 # " " of the second blob
##        self.time = time #time that the picture was taken
        
