# Class FaceDetector

'''
-------------face detection Lib using Dlib---------------
Dlib: C++ toolkit containing machine learning algorithms
face recognition: face detection and recognition open source
python library based on Dlib
'''

import face_recognition as fr
import cv2


class FaceDetector:
    def __init__(self, _scale=0.5):
        self._scale = _scale

    def detect(self, image):
        face_locs = []
        # Downsampling image for faster processing
        small_image = cv2.resize(image, (0, 0), fx=self._scale, fy=self._scale)
        # OpenCV color use BGR model; face_recognition use RGB color model
        rgb_small_image = cv2.cvtColor(small_image, cv2.COLOR_BGR2RGB)
        # rgb_small_image = small_image[:, :, ::-1]
        # Currently,use default HOG-based(Histogram of Oriented Gradients) model
        # It's a traditional object tracking method, but fairly accurate and fast
        # initialize the minimum and maximum (x, y)-coordinates

        face_locs = fr.face_locations(
            rgb_small_image, number_of_times_to_upsample=1)
        # CNN(convolutional neural network) model is more accurate, but too slow without GPU
        # face_locs = fr.face_locations(small_image, model="cnn")
        # (top, right, bottom, left) in locs
        filtered_face_locs = self.remove_invalid_face(image, face_locs)

        return filtered_face_locs

    def remove_invalid_face(self, original_image, all_locs):
        # print("face_locs: {}".format(all_locs))
        # print("face size: {} faces found.".format(len(all_locs)))
        new_locs = []
        if len(all_locs) > 0:
            for (top, right, bottom, left) in all_locs:
                (top1, right1, bottom1, left1) = (int(top/self._scale), int(right/self._scale),
                                                  int(bottom/self._scale), int(left/self._scale))
                new_locs.append((top1, right1, bottom1, left1))
                area = (bottom1 - top1) * (right1 - left1)
                var_lap = self.variance_of_laplacian(
                    original_image, (top1, right1, bottom1, left1))
                # print("var of lap: {}".format(var_lap))
                # print("face area: {}".format(area))
                if area < 3500 or area > 25000 or var_lap < 100:
                    new_locs.remove((top1, right1, bottom1, left1))

        return new_locs

    def variance_of_laplacian(self, original_image, loc):
        # compute the Laplacian of the image and then return the focus
        # measure, which is simply the variance of the Laplacian
        return cv2.Laplacian(original_image[loc[0]:loc[2], loc[3]:loc[1]], cv2.CV_64F).var()
