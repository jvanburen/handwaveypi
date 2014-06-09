#!/usr/bin/env python3
import bmap as yuv
from time import sleep
from io import BytesIO
from threading import Thread
from queue import Queue
import picamera


class FrameQueue(Thread, Queue):
    def __init__(self, width=200, height=200):
        Thread.__init__(self)
        Queue.__init__(self)

        self.dims = (width, height)
        self.cam = picamera.PiCamera()
        self.daemon = True

        self.cam.iso = 100
        self.cam.brightness = 40
        self.cam.color_effects = (128, 128)
        self.cam.hflip = True
        self.cam.meter_mode = 'matrix'
        self.cam.shutter_speed = 7500

        sleep(0.5) #wait for camera to update
    
    def run(self):
        stream = BytesIO()
        for foo in self.cam.capture_continuous(stream,
                                               format='yuv',
                                               resize=self.dims):
            stream.truncate()
            stream.seek(0)
            self.put(
                yuv.BrightnessMap(stream.getvalue(), *self.dims))
            
#    def get_frame(self):
#        return self.queue.get()
