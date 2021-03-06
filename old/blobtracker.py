from collections import deque, namedtuple
import datetime
from threading import Lock

class InitBlob:
    def __init__(self):
        self.prev = None
        
    def location(self):
        return None
    
    @staticmethod
    def timediff(m1, m2):
        return abs(m1.time - m2.time)

    @staticmethod
    def dist2(p1, p2):
        "distance squared"
        return (p1.r-p2.r)**2 + (p1.c-p2.c)**2
    

class Blob(InitBlob):
    def __init__(self, r, c, vr, vc, t, surface):
        self.r=r
        self.c=c
        self.vr=vr
        self.vc=vc
        self.time=t
        self.lock = Lock()
        self.surface = surface
        
    def fit(self, pos, time):
        "how likely it is that the given pos is a location of the blob at a given time"
        #1/distance squared
        if self.prev == None:
            return float('inf')
        with self.lock:
            return - BlobInfo.dist2(self.blob, pos) #IN PROGRESS

    def location(self, time):
        #thread safe
        "get the approximate location at the specified time"
        
        t = time - self.time
        if t < 0:
            return None
        return (self.r+self.vr*t, self.c+self.vc*t)

