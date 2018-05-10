#!/usr/bin/python3
# Office surveillance system
# @ZC zichun.lin@starasiatrading.com

'''
Normal Usage(surveillance and face recognition): 
python3 surveillance.py

Train a new classifier when face images databse changed:
python3 surveillance.py -t

Collect face images for training and saving:
python3 surveillance.py -c

Show help text:
python3 surveillance.py -h

Press 'q' for quit program
'''

from sql_updater import SqlUpdater
from motion_detector import MotionDetector
from face_detector import FaceDetector
from knn_classifier_train import KnnClassifierTrain
from knn_face_recognizer import KnnFaceRecognizer
from imutils.video import WebcamVideoStream
from imutils.video import FPS
from subprocess import call
import numpy as np
import argparse
import pickle
import datetime
import imutils
import time
import cv2

# Camera resolution setting
FRAME_WIDTH = 320
FRAME_HEIGHT = 240

# Construct the argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-t", "--train", help="train a KNN faces classifier", action="store_true")
ap.add_argument("-c", "--collect_faces", help="collect faces images for saving and training", action="store_true")
args = ap.parse_args()

if args.train:
    print("[INFO] Training KNN classifier...")
    knn_classifier_train = KnnClassifierTrain()
    knn_classifier_train.train(train_dir="faces/train", model_save_path="classifier/trained_knn_model.clf", n_neighbors=None)
    exit()
elif args.collect_faces:
    print("[INFO] Start to collect face images...")
    call(["python3", "face_collector.py"])
    print("[INFO] Collection Done.")
    exit()

# Declare user info dictionary
info_dict = {'NAME': '', 'DATETIME': '', 'ACTION': ''}

# Declare SqlUpdater and establish connection
sql_updater = SqlUpdater()
sql_connection, sql_cursor = sql_updater.connect()
# Delete all data in database table
# sql_updater.truncate(sql_connection, sql_cursor)  # Please comment it 

# Start camera videostream
print("[INFO] Starting camera...")
# 0 for default webcam, 1/2/3... for external webcam
video_stream = WebcamVideoStream(src=1)
video_stream.stream.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
video_stream.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
video_stream.start()
time.sleep(1.0)  # for warm up camera, 1 second

# Initialize motion detector
motion_detector = MotionDetector()
num_frame_read = 0  # no. of frames read

# Initialize face detector
face_detector = FaceDetector()

# Initialize face recognizer and load trained classifier
with open("classifier/trained_knn_model.clf", 'rb') as f:
    loaded_knn_clf = pickle.load(f)
knn_face_recognizer = KnnFaceRecognizer()

# FPS calculation
fps = FPS().start()

print("[INFO] Face Recognition is working...")

while True:
    # grab frame
    frame = video_stream.read()
    frame_show = frame.copy()
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_gray = cv2.GaussianBlur(frame_gray, (21, 21), 0)
    motion_locs = motion_detector.update(frame_gray)
    # form a nice average before motion detection
    if num_frame_read < 30:
        num_frame_read += 1
        continue

    timestamp = datetime.datetime.now()
    ts = timestamp.strftime("%Y-%m-%d %H:%M:%S")

    if len(motion_locs) > 0:
        # may consider to process in every other frame to accelerate
        # @(ZC)
        known_face_locs = face_detector.detect(frame)
        if len(known_face_locs) > 0:
            # print("[INFO] " + str(len(known_face_locs)) + " face found.")
            # Start face recognition
            predictions = knn_face_recognizer.predict(x_img=frame, x_known_face_locs=known_face_locs, knn_clf=loaded_knn_clf)
            for name, (top, right, bottom, left) in predictions:
                # print("- Found {} at ({}, {})".format(name, left, top))
                cv2.rectangle(frame_show, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.rectangle(frame_show, (left, bottom), (right, bottom+15), (0, 255, 0), -1)
                cv2.putText(frame_show, name, (int((right-left)/3)+left,bottom+12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
                info_dict['DATETIME'] = ts
                info_dict['NAME'] = name
                info_dict['ACTION'] = 'IN'
                if(sql_connection != None):
                    sql_updater.insert(sql_connection, sql_cursor, info_dict)
            '''
            # Draw green bounding box on faces in frame_show
            for top, right, bottom, left in known_face_locs:
                # Scale back up face locations
                top *= 1
                right *= 1
                bottom *= 1
                left *= 1
                cv2.rectangle(frame_show,(left, top), (right, bottom), (0, 255, 0), 2)
            '''
        # initialize the minimum and maximum (x, y)-coordinates
        (minX, minY) = (np.inf, np.inf)
        (maxX, maxY) = (-np.inf, -np.inf)

        # loop over the locations of motion and accumulate the
        # minimum and maximum locations of the bounding boxes
        for l in motion_locs:
            (x, y, w, h) = cv2.boundingRect(l)
            (minX, maxX) = (min(minX, x), max(maxX, x + w))
            (minY, maxY) = (min(minY, y), max(maxY, y + h))

        # draw red bounding box on moving body
        cv2.rectangle(frame_show, (minX, minY), (maxX, maxY), (0, 0, 255), 3)

    cv2.putText(frame_show, ts, (10, frame_show.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 1)
    cv2.imshow("Frame", frame_show)

    fps.update()

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

fps.stop()
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# Clean up and release memory
if sql_connection != None:
    sql_updater.close(sql_connection)
cv2.destroyAllWindows()
video_stream.stop()