import argparse
import bmap
import camerastream
import time
from blobs import get_blobs


def main():
    parser = argparse.ArgumentParser(description="Handwavey Pi 2014, see report for details.")
    parser.add_argument('frequency', metavar = 'freq', type=int, help="the number of samples per second")
    parser.add_argument('-v', '--verbose', metavar = '-v', action = "store_true")
    parser.add_argument('
