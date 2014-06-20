#!/usr/bin/env python3
import bmapfast as bm
import picamera
import queue
import time

class FrameQueue:
    def __init__(self, width, height):
        self.dims = (width, height)
        self.queue = queue.Queue()
        self.cam = picamera.PiCamera()
        self.cam.iso = 100
        self.cam.brightness = 40
        self.cam.color_effects = (128, 128)
        self.cam.hflip = True
        self.cam.meter_mode = 'matrix'
        self.cam.shutter_speed = 5000

        time.sleep(0.5) #wait for camera to update
    
    def run(self):
        stream = io.BytesIO()
        for foo in self.cam.capture_continuous(stream,
                                               format='yuv',
                                               resize=self.dims):
            stream.truncate()
            stream.seek(0)
            self.queue.put(
                bmap.BrightnessMap(stream.getvalue(), *self.dims))
            
    def get_frame(self):
        return self.queue.get()
        
    
