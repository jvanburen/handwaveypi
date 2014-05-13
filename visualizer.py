#!/usr/bin/env python3
import os
import sys
import pygame
import time
import queue
import bmapfast as bmap


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
                
    def update(self):
        pass

    def display_image(self, blobs):
        self.queue.put(blobs)




