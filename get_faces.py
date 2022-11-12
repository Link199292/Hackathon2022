from retinaface import RetinaFace
from deepface import DeepFace
from glob import glob
import cv2
import os

images_path = './output'
tmp_faces = './faces'
verifying = './verifying'

for pth in [tmp_faces, verifying]:
    if not os.path.exists(pth):
        os.mkdir(pth)


def compare_face(curr_face, other_faces_path, verify_folder, threshold):
    """
    :param curr_face: cv2.image(), the current image to be compared with the temp_img ones
    :param other_faces_path: str(), path with all the images to be compared with
    :param verify_folder: str(), path to use as a temporary storage for the curr_face
    :param threshold: float(), threshold
    :return:
    """
    other_faces_path = glob(f'{other_faces_path}/*')
    cv2.imwrite(f'{verify_folder}/face_0.jpg', curr_face)
    curr_face_path = f'{verify_folder}/face_0.jpg'
    if len(other_faces_path) > 0:
        for face in other_faces_path:
            ci = DeepFace.verify(curr_face_path, face, model_name='Facenet512',
                                 detector_backend='mtcnn',
                                 distance_metric='cosine',
                                 enforce_detection=False)
            if ci['distance'] > threshold:
                return curr_face
            else:
                return None
    else:
        return curr_face


def get_first_time_faces(image, t, threshold=0.9):
    """
    :param image: path of frames taken from a video
    :param t: datetime.datetime(), timestamp to store the image with
    :param threshold: float(), threshold to get whether two images are similar or not
    :return: None
    """
    idx = 0
    faces = RetinaFace.extract_faces(image, align=True)
    if len(faces) > 0:
        for face in faces:
            face = compare_face(face, tmp_faces, verifying, threshold=threshold)
            if face is not None:
                cv2.imwrite(f'{tmp_faces}/{idx}_{t}.jpg', face)
                idx += 1



