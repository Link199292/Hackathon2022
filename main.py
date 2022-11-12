import cv2
from datetime import datetime
import time
from get_faces import get_first_time_faces

url = 'rtsp://username:password@camera_ip_address:554/user=username_passw=password_channel=channel_n_stream=0.sdp'
out_path = './output'


def video_to_frames(in_path, out_path, threshold):
    """ Transforms video into multiple images (one for each frame) and,
        present, collect information from the faces.
    :param in_path: str(), link to a wifi webcam/camera
    :param out_path: str(), output_path for the unique faces
    :param threshold: float(), threshold to get whether two images are similar or not
    :return: None
    """
    full_video = cv2.VideoCapture(in_path)
    frame_idx = 0
    while True:
        success, frame = full_video.read()
        if not success:
            time.sleep(1)
            break
        t = datetime.now()
        cv2.imwrite(f'{out_path}/{frame_idx}_{t}.jpg', frame)
        get_first_time_faces(f'{out_path}/{frame_idx}_{t}.jpg', threshold)
        frame_idx += 1
    full_video.release()


if __name__ == '__main__':
    video_to_frames(url, out_path, threshold=0.8)
