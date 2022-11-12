from time import sleep
from datetime import datetime
import numpy as np
import cv2
from PIL import Image
from glob import glob
from facelib import FaceDetector, AgeGenderEstimator, EmotionDetector
from pymongo import MongoClient as Client


class CustomerData:
    def __init__(self, collection):
        self.collection = collection
        self.age_gender = AgeGenderEstimator()
        self.emotion = EmotionDetector()

    # extract features from images
    def extract_info(self, img_path, img_time):
        img = cv2.imread(img_path)
        detector = FaceDetector()
        faces, boxes, scores, landmarks = detector.detect_align(img)

        if faces.dim() != 4:
            return

        genders, ages = self.age_gender.detect(faces)
        emotions, probab = self.emotion.detect_emotion(faces)

        out = [{"time": img_time, "gender": genders[i], "age": ages[i], "emotion": emotions[i]} for i in
               range(len(ages))]

        return out

    # write extracted data to mongodb
    def write_to_mongo(self, info_data):
        print(info_data)
        db = self.collection
        db.insert_many(info_data)


if __name__ == "__main__":
    client = Client("mongodb://127.0.0.1/")
    collection = client.shop.customers
    img_path = "./faces/"

    img_done = set()

    C = CustomerData(collection)
    while True:
        imgs_path = set(glob(img_path + "*.jpg"))
        for image in imgs_path:
            if image not in img_done:
                t = image.split("_")[-1].replace("jpg", "")  # get image time
                data = C.extract_info(image, t)    # extract metadata
                C.write_to_mongo(data)  # save data into MongoDB collection
                img_done.add(image)     # add image path to done images
                print(data)
