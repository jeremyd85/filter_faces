import os
import cv2
from cv_image import Image

ME_FILEPATH = 'jeremy'
KNOWN_PATH = 'known_faces'

def _get_face(point, faces):
    p_x = point[0]
    p_y = point[1]
    for (x1, y1, w, h) in faces:
        x2 = x1+w
        y2 = y1+h
        if p_x >= x1 and p_x <= x2 and p_y >= y1 and p_y <= y2:
            return [(x1, y1), (x2, y2)]
    return []

@staticmethod
def crop_handler(event, x, y, flags, param):
    print("clicked!")
    img = param[0]
    known_path = os.path.join(KNOWN_PATH, ME_FILEPATH)
    if not os.path.exists(known_path):
        os.mkdir(known_path)
    if event == cv2.EVENT_LBUTTONDBLCLK:
        faces = img.get_faces()
        face_points = _get_face((x, y), faces)
        if face_points:
            face_img = Image(cv_image=img.crop(face_points[0], face_points[1]))
            face_img.create_image(known_path)