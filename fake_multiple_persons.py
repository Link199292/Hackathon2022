from glob import glob
import random
from PIL import Image

input_path = '/media/link92/E/pythonProject/hackaton/original_images'
out_path = '/media/link92/E/pythonProject/hackaton/fake_video_frames'


def concat(im1, im2):
    """
    :param im1: PIL.Image()
    :param im2: PIL.Image()
    :return: PIL.Image()  # Vertically merged
    """
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst


def create_fake_frames(input_path):
    """ Starting from images, it produces a sequence of frames of people.
    :param str path to fake frames of video
    :return: None
    """
    images = glob(f'{input_path}/**/*.png')
    random.shuffle(images)
    idx = 0
    while images:
        take_two = random.random() > 0.5
        if take_two and len(images) > 1:
            img1, img2 = Image.open(images.pop()).convert('RGB'), Image.open(images.pop()).convert('RGB')
            merged = concat(img1, img2)
            merged.save(f'{out_path}/{idx}.jpg')
        else:
            img = Image.open(images.pop()).convert('RGB')
            img.save(f'{out_path}/{idx}.jpg')
        idx += 1


create_fake_frames(input_path)

