from time import sleep
from datetime import datetime
import numpy as np
import cv2
from PIL import Image
from facelib import FaceDetector, AgeGenderEstimator, EmotionDetector
from pymongo import MongoClient as Client


class StreamCustomerData:
    def __init__(self, collection):
        self.collection = collection
        self.age_gender = AgeGenderEstimator()
        self.emotion = EmotionDetector()

    # add face check
    def face_check(self, frame):
        pass

    # extract features from images
    def extract_info(self, img, img_time):
        detector = FaceDetector()
        faces, boxes, scores, landmarks = detector.detect_align(img)

        if faces.dim() != 4:
            return

        genders, ages = self.age_gender.detect(faces)
        emotions, probab = self.emotion.detect_emotion(faces)

        out = [{"time": img_time, "gender": genders[i], "age": ages[i], "emotion": emotions[i]} for i in range(len(ages))]

        return out

    # write extracted data to mongodb
    def write_to_mongo(self, info_data):
        print(info_data)
        db = self.collection
        db.insert_many(info_data)


if __name__ == "__main__":
    client = Client("mongodb://127.0.0.1/")
    collection = client.shop.customers

    # streaming
    video = cv2.VideoCapture('rtsp://username:password@camera_ip_address:554/user=username_passw=password_channel=channel_n_stream=0.sdp')

    # saved video
    # video = cv2.VideoCapture("filename")

    C = StreamCustomerData(collection)
    while True:
        ret, frame = video.read()
        if frame is None:
            sleep(1)
            ret, frame = video.read()
            if frame is None:
                break

        t = datetime.now()
        # cleaned_frame = C.face_check(frame)
        # data_extracted = []
        # for f in cleaned_frame:
        data = C.extract_info(frame, t)
        # data_extracted.append(data)
        C.write_to_mongo(data)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video.release()

