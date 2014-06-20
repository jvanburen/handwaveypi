#!/usr/bin/env python3
import argparse
import bmap
import camerastream
import time
from blobs import get_blobs, ImageBlob
import signal
import struct
import sys

COPYRIGHT = """THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."""

def sleep_indefinitely():
    while True:
        time.sleep(1)

## Arguments are mostly camera-related
## there's frequency (FPS) or trigger (for capturing on system calls)
## There's resolution
## there's verbosity (for manual output) OR there's struct format for programmatic access to output


def _create_arg_parser():
    parser = argparse.ArgumentParser(
        description="Handwavey Pi 2014, see report for details.",
        epilog="Jacob Van Buren 2014. Licensed under BSD 3-clause license." + COPYRIGHT)

    parser.add_argument('resolution', type=int, default=50,
        help = "Horizontal & vertical resolution of raw camera images. Higher numbers give slightly better accuracy, but take quadratically longer to process")
    ##capturing = parser.add_mutually_exclusive_group()
    ##capturing.add_argument('frequency', type=int, default=2,
    ##    help="The number of samples per second. Might actually be fewer, but not more. If zero, takes a picture every time SIGINFO is received.")
    ##capturing.add_argument('-tr', '--trigger', action = 'store_true',
    ##    help ="Takes a picture when the process receives SIGINFO")
    parser.add_argument('frequency', type=float, default=2,
        help="The number of samples per second. Might actually be fewer, but not more. If zero, takes a picture every time SIGINFO is received. If -1, takes a picture every time Enter is pressed.")

    parser.add_argument('-v', '--verbose', action = "store_true",
        help = "outputs very human readable info")
    return parser

def _main():
    parser = _create_arg_parser()
    global args
    args = parser.parse_args()

    
    if args.resolution < 10:
        print("Resolution must be > 10.", file=sys.stderr)
        exit(1)
    if args.frequency < 0 and args.frequency != -1:
        print("Frequency must be > 0 for timed capture, zero for signal capture, or -1 for keyboard capture.", file=sys.stdout)
        exit(1)
    
    use_signal = args.frequency == 0
    use_keyboard = args.frequency == -1
    if not use_signal and not use_keyboard:
        time_per_frame = 1/args.frequency
    
    if not args.verbose:
        sys.stdout.detach()

    global _fq
    _fq = camerastream.FrameQueue(args.resolution, args.resolution, use_signal or use_keyboard)
    _fq.start()
    if use_signal and hasattr(signal, 'SIGINFO'):
        signal.signal(signal.SIGINFO, take_picture)
        sleep_indefinitely()
        return # never reached
    elif use_keyboard:
        while True:
            s = input()
            take_picture()
        return # never reached
    import pygame###
    window = pygame.display.set_mode((200, 200))###
    pxs = pygame.PixelArray(window)###
    while True:
        starttime = time.clock()
        take_picture()
        frame = take_picture()###
        frame.draw_to_screen(pxs)###
        pygame.display.flip()
        
        lag = time.clock() - starttime
        
        if lag < time_per_frame:
            time.sleep(time_per_frame)
 
def take_picture(*unused):  
    #print("take_picture")
    starttime = time.clock()
    _fq.notify()
    frame = _fq.get()
    blobs = get_blobs(frame)
    
    if args.verbose:
        output = make_ascii_output(blobs, starttime)
    else:
        output = make_c_struct(blobs, starttime)
    #print('took picture')
    sys.stdout.write(output)
    return frame ###


def make_c_struct(blobs, starttime):
    buffer = bytearray(1 + 4 +ImageBlob.STRUCT.size*2)
    if len(blobs) < 2:
        struct.pack_into(">i", buffer, 1, round((time.clock()-starttime)*1000))
        return buffer
    buffer[0] = 1
    struct.pack_into(">i", buffer, 1, round((time.clock()-starttime)*1000))
    blobs[0].pack_into(buffer, 1+4)
    blobs[1].pack_into(buffer, 1+4+ImageBlob.STRUCT.size)
    return buffer

def make_ascii_output(blobs, starttime):
    l = []
    if len(blobs) < 2:
        l.append("No blobs found")
    else:
        l.append("Blobs Found")
        l.append('Blob 0:\t' + str(blobs[0]))
        l.append('Blob 1:\t' + str(blobs[1]))

    l.append('Lag:\t' + str(int(round((time.clock()-starttime)*1000)))+'ms')
    return '\n'.join(l)+'\n\n'
    

if __name__=='__main__':
    _main()







