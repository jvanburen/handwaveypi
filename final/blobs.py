from collections import deque
import bmap

class ImageBlob:
    def __init__(self, pixels, width, height):
        from math import pi, sqrt
        #scale pixels linearly to be in [-1, 1]
        units_per_row = 2.0/height
        units_per_column = 2.0/width
        average_units_per_dim = units_per_row/2 + units_per_column/2
        self.radius = average_units_per_dim * sqrt(len(pixels)/pi) #take the average to get a decent looking circle for a non-square image
        coords = list(map(lambda i: (units_per_row * (i//width) - 1, units_per_column * (i%width)-1), pixels))
        rows, cols = zip(*coords)
        avg_row = sum(rows)/len(rows)
        avg_col = sum(cols)/len(cols)
        
        self.center = (avg_col, avg_row) # (x, y) coordinate system
    def __str__(self):
        return "Blob at ({}, {}), with radius {}".format(self.center[0], self.center[1], self.radius)
    def __repr__(self):
        return "<Blob object at ({}, {}), with radius {}>".format(self.center[0], self.center[1], self.radius)

def get_blobs(frame, threshold = 0.5, count = -1):
    def get_adj(frame, i):
        adj = []
        r, c = i//frame.width, i%frame.width
        if r+1 < frame.height: adj.append(i+frame.width)
        if r-1 >= 0: adj.append(i-frame.width)
        if c+1 < frame.width: adj.append(i+1)
        if c-1 >= 0: adj.append(i-1)
        return adj
    FG = frozenset(i for i, v in enumerate(frame) if v > threshold)
    unvisited = frozenset(FG)
    blobs = set()
    while unvisited:
        visited = set()
        queue = deque()
        s = next(iter(unvisited))
        queue.append(s)
        visited.add(s)
        while queue:
            t = queue.popleft()
            for v in get_adj(frame, t):
                if v in visited \
                   or v not in FG:
                    continue
                visited.add(v)
                queue.append(v)
        blobs.add(frozenset(visited))
        unvisited ^= visited
    #just a check
    #it's worked every time i've tried it and it looks right so
##        allblobs = set()
##        for b in blobs:
##            allblobs |= b
##        assert allblobs == FG
    
    blob_pixels = sorted(blobs, key=len, reverse=True)
    
    if count >= 0:
        blob_pixels = blob_pixels[:count]
   
    blobs = [ImageBlob(pixels, frame.width, frame.height) for pixels in blob_pixels]
    
    return blobs



