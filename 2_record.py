import picamera
import time
import datetime

def record():
  with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)
    now = datetime.datetime.now()
    filename = now.strftime('%Y-%m-%d %H:%M:%S')
    camera.start_recording(output = filename + '.h264') #h.264 코덱
    camera.wait_recording(5)
    camera.stop_recording()
    
    
while True:
  record()
