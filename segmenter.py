import Graphmodified as NetworkFlow
import grid
from math import *
G = None

#
# a and b are both [0,1] -> [0,1]
# p is [0,1] x [0,1] -> [0,1]
#
#

MAX_VAL = 9
RESOLUTION = 0.01
RES_FACTOR = int(round(1/RESOLUTION))

def scaled(f):
    def new(*args, maxval=None):
        if maxval:
            MAX_VAL = maxval
        else:
            global MAX_VAL
        return round(RES_FACTOR * f(*map(lambda x: x/MAX_VAL, args)))
    return new

@scaled
def a(x):
    "Pr[px w/ val x is in a blob]"
    #return math.sqrt(x)
    return (1-cos(4*x**2))/2

@scaled
def b(x):
    "Pr[px w/ val x is in the background]"
    return 1 - sqrt(x)

@scaled
def p(x, y):
    #should be the same as p(y, x)
    "penalty for making adj. pxs w/ vals x & y end up in different segments"
    #i.e. how similar they are
    def transform(x):
        x /= MAX_VAL
        return MAX_VAL * (-cos(pi*x)+1)/2
    diff = abs(transform(x)-transform(y))
    return diff**2
    #return (-cos(pi*diff**2)+1)/2



def get_test_image(string):
    WIDTH = string.strip().find('\n')
    string = string.strip().replace('\n', '')
    HEIGHT = len(string) // WIDTH
    data = bytes(map(lambda x: int(x,16), string))
    image = grid.Grid(data, WIDTH, HEIGHT)
    return image
    
#image = grid.Grid(brightness, WIDTH, HEIGHT)
def get_segmentation(image):
    global G
    G = NetworkFlow.FlowNetwork(len(image)+2)
    image_vertices = tuple(range(len(image)))
    S = len(image)
    T = S + 1

    #add S edge, then T edge, then incoming edges between
    for v in image_vertices:
        G.add_edge(S, v, w=a(image[v]))
        G.add_edge(v, T, w=b(image[v]))
        for u in image.get_adj(v):
            G.add_edge(u, v, w=p(image[u], image[v]))
    return G.min_cut(S, T)

def visualize(image, segmentation):
    s = []
    for r in range(image.HEIGHT):
        for c in range(image.WIDTH):
            if image.to_index((r,c)) in segmentation[0]:
                s.append('#')
            else:
                s.append(' ')
        s.append('\n')
    print(''.join(s))

def quicktest(string, randomize= True):
    global MAX_VAL
    import time
    image = get_test_image(string)
    MAX_VAL = max(image.values)
##    import random
##    #randomize
##    if randomize:
##        copy = bytearray(image.values)
##        for i in range(len(image)):
##            if random.random()**4 * MAX_VAL > copy[i]:
##                copy[i] = int(random.random()**3*MAX_VAL)
##        image.values = bytes(copy)
##
##        print("randomized:")
##        for r in range(image.HEIGHT):
##            for c in range(image.WIDTH):
##                print(image[i], end='')
##            print()
##
##        print()
    start = time.clock()
    seg = get_segmentation(image)
    dur = time.clock() - start
    visualize(image, seg)
    print("took " + str(round(dur*1000)) + 'ms')
        
        
