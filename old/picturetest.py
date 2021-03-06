from bmap import *
import picamera
from time import sleep
import queue, io

with picamera.PiCamera() as cam:
    cam.led = False
    cam.iso = 100
    cam.brightness = 40
    cam.color_effects = (128, 128)
    cam.hflip = True
    cam.meter_mode = 'matrix'
    cam.shutter_speed = 5000

    frames = queue.Queue(maxsize = 10)
    sleep(1) #Give the camera time to calibrate

    stream = io.BytesIO()
    photostream = cam.capture_continuous(stream, format='yuv', resize=(240, 180))
    for i in range(10):
        stream.truncate()
        stream.seek(0)
        foo = next(photostream)
        frames.put(BrightnessMap(stream.getvalue(), 240, 180))

