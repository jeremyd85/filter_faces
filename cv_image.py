import cv2
import copy
from PyQt5.QtGui import QImage, QPixmap

CLASSIFIER = '/home/jeremy/code/C++Projects/opencv/data/haarcascades/haarcascade_frontalface_default.xml'


class Image():

    def __init__(self, file_path='', cv_image=None):
        self.file_path = file_path
        self.img = cv2.imread(file_path) if file_path else cv_image

    @property
    def width(self):
        return self.img.shape[1]

    @property
    def height(self):
        return self.img.shape[0]

    def scale(self, scale_factor):
        return Image(cv_image=cv2.resize(self.img_copy, (int(self.width * scale_factor), int(self.height * scale_factor))))

    def grayscale(self):
        return Image(cv_image=cv2.cvtColor(self.img_copy, cv2.COLOR_BGR2GRAY))

    def get_faces(self):
        face_cascade = cv2.CascadeClassifier(CLASSIFIER)
        faces = face_cascade.detectMultiScale(
            image=self.grayscale().img,
            scaleFactor=1.3,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        return [[(x1, y1), (x1+w, y1+h)] for (x1, y1, w, h) in faces]

    def get_face_at_point(self, point):
        p_x = point[0]
        p_y = point[1]
        faces = self.get_faces()
        for [(x1, y1), (x2, y2)] in faces:
            if p_x >= x1 and p_x <= x2 and p_y >= y1 and p_y <= y2:
                return [(x1, y1), (x2, y2)]
        return []

    def rectangle(self, point1, point2):
        return Image(cv_image=cv2.rectangle(self.img_copy, point1, point2, (0, 0, 255), 4))

    def crop(self, point1, point2):
        cropped_img = self.img[point1[1]:point2[1], point1[0]:point2[0]]
        return Image(cv_image=cropped_img)

    def create_image(self, path):
        self.file_path = path
        print(path)
        cv2.imwrite(path, self.img)

    def to_rgb(self):
        return Image(cv_image=self.img[:, :, ::-1])

    def vertical_flip(self):
        return Image(cv_image=cv2.flip(self.img, 1))

    def get_pixmap(self):
        image = QImage(self.img, self.width, self.height, 3*self.width, QImage.Format_RGB888)
        return QPixmap(image)

    @property
    def img_copy(self):
        return copy.deepcopy(self.img)



