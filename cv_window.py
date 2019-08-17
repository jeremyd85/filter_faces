import cv2
import handlers
from cv_image import Image


class Window:
    def __init__(self, name, video=False):
        self.name = name
        self.closed = False
        self.video_capture = cv2.VideoCapture(0) if video else None
        self.frame = None
        cv2.namedWindow(name, cv2.WINDOW_NORMAL)

    def update_image(self, image):
        self.frame = image
        cv2.imshow(self.name, image.img)
        print(self.frame)

    def close_after_key(self, key):
        if cv2.waitKeyEx(0) == key:
            self.close()

    def close(self):
        if self.video_capture:
            self.video_capture.release()
        cv2.destroyAllWindows()
        self.closed = True

    def mouse_event(self, handler_fun, param=[]):
        cv2.setMouseCallback(self.name, handler_fun, param=param)

    def get_frame(self):
        if not self.video_capture:
            return []
        return_val, self.frame = self.video_capture.read()
        return Image(cv_image=self.frame)


