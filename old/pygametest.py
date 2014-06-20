

import os
import sys
import pygame
from pygame.locals import *
import time
import queue
import bmapfast as bmap
import threading
import random


def setup_video_driver():
    if os.getenv("DISPLAY"):
        try:
            pygame.display.init()
        except pygame.error:
            print('no X server available', file=sys.stderr)
        else:
            return pygame.display.Info()

    
    for driver in ('fbcon', 'directfb', 'svgalib'):
        # Make sure that SDL_VIDEODRIVER is set
        if not os.getenv('SDL_VIDEODRIVER'):
            os.putenv('SDL_VIDEODRIVER', driver)
        try:
            pygame.display.init()
        except pygame.error:
            print('Driver: {0} failed.'.format(driver), file=sys.stderr)
        else:
            break
    else:
        raise OSError('No suitable video driver found!')
    return pygame.display.Info()

def setup_GUI():
    pygame.mouse.set_visible(False)

def should_quit():
    return pygame.key.get_mods() & KMOD_CTRL \
       and pygame.key.get_pressed()[K_q]

class Visualizer:
    def __init__(self, width, height, zoom=True):
        self.width = width
        self.height = height
        
        self.zoom = zoom
        if zoom:
            self.width *= 2
            self.height *= 2
        self.queue = queue.Queue(5)
        

    def run(self):
        info = setup_video_driver()
        window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Visualizer")
        while pygame.event.poll().type != pygame.QUIT:
            print("running!")
            try:
                blobs = self.queue.get(timeout=0.020)
                if self.zoom:
                    pygame.transform.scale2x(blobs.surface, window)
                else:
                    window.blit(image.surface, (0,0))
                    
            except queue.Empty:
                pass
            finally:
                pygame.display.flip()

    def display_image(self, blobs):
        self.queue.put(blobs)

        
def run(size, zoom = True):
    if zoom:
        size = tuple(map(lambda x:x*2, size))
    info = setup_video_driver()
    window = pygame.display.set_mode(size)
    pygame.display.set_caption("Visualizer")
    while pygame.event.poll().type != pygame.QUIT:
        try:
            s = get_surface(size)
            if zoom:
                pygame.transform.scale2x(surface, window)
            else:
                window.blit(surface, (0,0))
        finally:
            pygame.display.flip()

def get_surface(size):
    s = pygame.Surface(size)
    px = pygame.PixelArray(s)
    for c in range(s.get_width()):
            for r in range(s.get_height()):
                    px[r,c] = (random.randint(0, 0xFF))*3
    return s

def test_static(t=10):
	import random
	class NotBlobs:
		pass
	class NotImage:
		pass
	v = start_running(240, 180)
	start = time.clock()
	while time.clock() < start+t:
		s = pygame.Surface((v.width, v.height))
		px = pygame.PixelArray(s)
		for c in range(v.width):
			for r in range(v.height):
				px[r,c] = (random.randint(0, 0xFF))*3
		b  = NotBlobs()
		b.image = NotImage()
		b.image.surface = s
		v.display_image(b)
	exit()

if __name__ == '__main__':
	if len(sys.argv)>=2 and sys.argv[1] == '--test_static':
		n = 10
		if len(sys.argv)>=3:
			n=int(sys.argv[2])
		test_static(n)
