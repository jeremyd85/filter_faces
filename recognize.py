import face_recognition
import os
from cv_window import Window
from cv_image import Image

KNOWN_FACES = 'known_faces'


class Recognizer:

    def __init__(self, name, max_images=10):
        self.name = name
        self.known_path = os.path.join(KNOWN_FACES, name)
        self.max_images = max_images
        self.encodings = []

    def _get_known_list(self):
        known_list = os.listdir(self.known_path)
        if len(known_list) > self.max_images:
            known_list = known_list[:self.max_images]
        return known_list

    def get_encodings(self):
        if not self.encodings:
            known_list = self._get_known_list()
            for image in known_list:
                loaded_image = face_recognition.load_image_file(image)
                self.encodings.append(face_recognition.face_encodings(loaded_image))
        return self.encodings


def main():
    win = Window('Recognize', video=True)
    win.close_after_key(27)
    while not win.close:
        win.update_image(win.get_frame())

main()



