#!/usr/bin/env python3
import bmap as yuv
from time import sleep
from io import BytesIO
from threading import Thread, Event
from queue import Queue
import picamera


class FrameQueue(Thread, Queue):
    def __init__(self, width=200, height=200, wait=False):
        Thread.__init__(self)
        Queue.__init__(self)

        self.dims = (width, height)
        self.cam = picamera.PiCamera()
        self.waiting = Event() if wait else None
        self.daemon = True

        self.cam.iso = 100
        self.cam.brightness = 40
        ##self.cam.color_effects = (128, 128)
        self.cam.hflip = True
        self.cam.vflip = True
        ##self.cam.meter_mode = 'matrix'
        self.cam.shutter_speed = 7500

        sleep(0.5) #wait for camera to update
    
    def run(self):
        stream = BytesIO()
        camera_stream = self.cam.capture_continuous(stream,
                                               format='yuv',
                                               resize=self.dims)
        for foo in camera_stream:
            if self.waiting is not None:
                self.waiting.clear()
            stream.truncate()
            stream.seek(0)
            if self.qsize() >= 2:
                try: self.get(block=False)
                except Empty: pass
            self.put(yuv.BrightnessMap(stream.getvalue(), *self.dims))

            if self.waiting is not None:
                self.waiting.wait()
                #print('done waiting!')

    def notify(self):
        if self.waiting is not None:
            self.waiting.set()

#    def get_frame(self):
#        return self.queue.get()
