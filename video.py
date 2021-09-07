import time
import numpy as np
import cv2
import base64
from imutils.video import VideoStream
import threading
import detection
import field

# Limitting the output period
min_period = 1/30
# Image retrieve and processing duration
period = None
# Current capture
capture = None
# The last retrieved image
image = None
# Debug output
debug = False
# Ask main thread to stop capture
stop_capture = False

def listCameras():
    indexes = []
    for index in range(10):
        cap = cv2.VideoCapture(index)
        if cap.read()[0]:
            indexes.append(index)
            cap.release()
    return indexes

def startCapture(index):
    global captures, capture, image

    capture = VideoStream(src=index, framerate=25)
    capture.stream.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
    capture.stream.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
    capture.start()

    time.sleep(0.1)
    return image is not None

def stopCapture():
    global stop_capture
    stop_capture = True

def setCameraSettings(brightness, contrast, saturation):
    if capture is not None:
        capture.stream.stream.set(cv2.CAP_PROP_BRIGHTNESS, brightness)
        capture.stream.stream.set(cv2.CAP_PROP_CONTRAST, contrast)
        capture.stream.stream.set(cv2.CAP_PROP_SATURATION, saturation)

def thread():
    global capture, image, period, stop_capture
    while True:
        if capture is not None:
            t0 = time.time()
            image_captured = capture.read()

            if image_captured is not None:
                # Process the image
                detection.detectAruco(image_captured, debug)
                detection.detectBall(image_captured, debug)
                detection.publish()

            # Computing time
            current_period = time.time() - t0
            if current_period < min_period:
                time.sleep(min_period - current_period)
            current_period = time.time() - t0

            if period is None:
                period = current_period
            else:
                period = period*0.99 + current_period*0.01

            if image_captured is None:
                capture = None

            image = image_captured

            if stop_capture:
                stop_capture = False
                capture.stop()
                del capture
                capture = None
                image = None
        else:
            time.sleep(0.1)

def getImage():
    global image
    if image is not None:
        data = cv2.imencode('.jpg', image)
        return base64.b64encode(data[1]).decode('utf-8')
    else:
        return ''

def getVideo(with_image):
    global period
    data = {
        'running': capture is not None,
        'fps': round(1/period, 2) if period is not None else 0,
        'detection': detection.getDetection(),
    }

    if with_image:
        data['image'] = getImage()

    return data

# Listing available cameras
cameras = listCameras()

# Starting the video processing thread
video_thread = threading.Thread(target=thread)
video_thread.start()
