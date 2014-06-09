import threading
import bmap
import camerastream
import time


from blobs import get_blobs
def main(n=10):
	fq = camerastream.FrameQueue(100, 100)
	fq.start()
	
	for i in range(n):
		print("-"*40)
		print("run %d of %d"%(i+1,n))
		frame = fq.get() 
		blobs = get_blobs(frame)
		for blob in blobs:
			print(blob)
		print("took {} seconds".format(time.time() - frame.timestamp))

if __name__ == '__main__':
	main()

