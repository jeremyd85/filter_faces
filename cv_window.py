import cv2
import handlers


class Window:
    def __init__(self, name):
        self.name = name
        self.closed = False
        cv2.namedWindow(name, cv2.WINDOW_NORMAL)

    def update_image(self, image):
        cv2.imshow(self.name, image.img)

    def close_after_key(self, key):
        if cv2.waitKeyEx(0) == key:
            cv2.destroyAllWindows()
            self.closed = True

    def close(self):
        cv2.destroyAllWindows()

    def mouse_event(self, handler_fun, param=[]):
        cv2.setMouseCallback(self.name, handler_fun, param=param)

