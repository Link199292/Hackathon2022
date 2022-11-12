from retinaface import RetinaFace
from deepface import DeepFace
from glob import glob
from PIL import Image
import cv2
import os

images_path = '/media/link92/E/pythonProject/hackaton/fake_video_frames'
tmp_faces = '/media/link92/E/pythonProject/hackaton/tmp_faces'
verifying = '/media/link92/E/pythonProject/hackaton/verifying'

for pth in [tmp_faces, verifying]:
    if not os.path.exists(pth):
        os.mkdir(pth)


def get_first_time_faces(images, similarity_thresh=0.007):
    """
    :param images: path of frames taken from a video
    :param similarity_thresh: threshold to get whether two images are similar or not
    :return: None
    """
    # Get fake frames
    images = glob(f'{images_path}/*')
    # sort by integer value
    images.sort(key=lambda x: int(x.split('/')[-1].replace('.jpg', '')))
    idx = 0
    # for each frame
    for image in images:
        # detect the face location
        faces = RetinaFace.extract_faces(image, align=True)
        # if faces are detected
        if len(faces) > 0:
            for face in faces:
                cv2.imwrite(f'{tmp_faces}/{idx}.jpg', face)
                idx += 1
