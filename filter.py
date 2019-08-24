import numpy as np
import cv2

import os
from cv_image import Image
from cv_window import Window

import shutil


class ImageFilter:

    KNOWN_PATH = 'known_faces'

    def __init__(self, name, input_path):
        self.curr_image = Image()
        self.name = name
        self.input_path = input_path
        self.image_list = self.get_image_list()
        self.output_path = os.path.join(ImageFilter.KNOWN_PATH, name)
        self.img_count = 0
        self.scale = 0.25
        self.window = None
        self._setup_dirs()

    def start_window(self):
        self.window = Window(self.name)
        self.window.mouse_event(self.crop_handler)
        self._update_window()
        self.window.close_after_key(27, stay_open=True)

    def _setup_dirs(self):
        if not os.path.exists(ImageFilter.KNOWN_PATH):
            os.mkdir(ImageFilter.KNOWN_PATH)
        if os.path.exists(self.output_path):
            shutil.rmtree(self.output_path)
        os.mkdir(self.output_path)

    def crop_handler(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            x = x / self.scale
            y = y / self.scale
            face_points = self.curr_image.get_face_at_point((x, y))
            if face_points:
                face_img = self.curr_image.crop(face_points[0], face_points[1])
                output_file = os.path.join(self.output_path, '{0}{1}.png'.format(self.name, self.img_count))
                face_img.create_image(output_file)
            self.img_count += 1
            self._update_window()

    def get_image_list(self):
        if os.path.exists(self.input_path):
            image_list = os.listdir(self.input_path)
            return [os.path.join(self.input_path, f) for f in image_list]
        else:
            return []

    def _update_window(self):
        if self.img_count == len(self.image_list):
            self.window.close()
        self.curr_image = Image(file_path=self.image_list[self.img_count])
        display_img = Image(cv_image=self.curr_image.img_copy)
        faces = display_img.get_faces()
        display_img = display_img.scale(self.scale)
        for [point1, point2] in faces:
            point1 = (int(point1[0] * self.scale), int(point1[1] * self.scale))
            point2 = (int(point2[0] * self.scale), int(point2[1] * self.scale))
            display_img = display_img.rectangle(point1, point2)
        self.window.update_image(display_img)


def filter_dir(dirname):
    name = os.path.basename(dirname)
    img_filter = ImageFilter(name, dirname)
    img_filter.start_window()
