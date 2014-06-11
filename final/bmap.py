from array import array
import datetime
from collections import deque
from ctypes import *
import sys
import time
import urllib.error
from urllib.request import urlopen

class BrightnessMap:
    """
An object with a timestamp, raw data, and processed data


"""
    normalizer = CDLL("./normalizer.so")
    NORMALIZE = True
    
    def __init__(self, data, width, height):
        self.timestamp = time.time()
        width, height = int(width), int(height)
        if width <= 0: raise ValueError("width must be > 0")
        if height <= 0: raise ValueError("height must be > 0")

        self._w = width
        self._h = height

        self._c_data_type = c_double * (width*height)

        if isinstance(data, str):
            #interpret data as a location
            loc = data
            try:
                with open(loc, 'rb') as f:
                    self._raw = f.read()
            except IOError:
                try:
                    self._raw = urlopen(loc).readall()
                except:
                    raise ValueError("Could not interpret input as a location on the local computer or the internet")
        else:
            self._raw = bytes(data)

        self._unenhanced = bytes(type(self).process_raw(self._raw, self._w, self._h))
        a = array('d')
        a.extend(self._unenhanced)
        type(self).scale_data(a)
        self._data = a

        if type(self).NORMALIZE:
            self.normalize()
        assert len(self._data) == self._w * self._h
        
        
            
    @classmethod
    def process_raw(cls, raw, width, height):
        "gets brightness data from a raw YUV file"
        from math import ceil
        
        data = bytearray()
        btsperrow = 32*ceil(width/32) #increase to a multiple of 32
        for row in range(height):
            i = row*btsperrow
            data.extend(raw[i:i+width])

        return data

    @classmethod
    def scale_data(cls, data):
        "scales data linearly to fill the interval [0, 1]"
        minval = min(data)
        maxval = max(data)

        if maxval == minval:
            return
        if minval == 0.0 and maxval== 1.0:
            return
        
        maxval -= minval
        for i, v in enumerate(data):
            data[i] = (v-minval)/maxval
    
    
    def normalize(self):
        "heuristically reduces noise"
        values = array('d')
        buffer = self._c_data_type()
        data = self._c_data_type(*self._data)
        w = c_int(self._w)
        h = c_int(self._h)
        thresh = 0.5
        hpf_level = c_double(thresh)
        type(self).normalizer.normalize(buffer, data, w, h, hpf_level)
        values.extend(buffer)
        type(self).scale_data(values)
        self._data = values
        
    def draw_to_screen(self, pxarray):
        for i, v in enumerate(self._data):
            v = int(v*0xff)
            pxarray[i%self._w, i//self._w] = (v,v,v)
    
    @property
    def _dim(self):
        return (self._w, self._h)
    @property
    def width(self):
        return self._w
    @property
    def height(self):
        return self._h

    def to_coord(self, index):
        return (index//self._w, index%self._w)
    def __getitem__(self, index):
        return self._data[index]
    def __setitem__(self, index, value):
        self._data[index] = value
    def __len__(self):
        return len(self._data)
    def __iter__(self):
        return iter(self._data)

