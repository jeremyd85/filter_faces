import face_recognition
import os
from cv_window import Window
from cv_image import Image
import cv2
import numpy as np
import csv


class Recognizer:

    KNOWN_FACES = 'known_faces'

    def __init__(self, name='', max_images=10):
        self.name = name
        self.known_path = os.path.join(Recognizer.KNOWN_FACES, name)
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
                path = os.path.join(self.known_path, image)
                loaded_image = face_recognition.load_image_file(path)
                self.encodings.append(face_recognition.face_encodings(loaded_image)[0])
        return self.encodings

    @staticmethod
    def make_recognizer(img, name):
        name = name.lower()
        known_list = os.listdir(Recognizer.KNOWN_FACES)
        if name in known_list:
            return
        else:
            base_path = os.path.join(Recognizer.KNOWN_FACES, name)
            os.mkdir(base_path)
            pic_path = os.path.join(base_path, "{0}0.png".format(name))
            img.create_image(pic_path)
        return Recognizer(name)


class RecognizeFaces():

    def __init__(self, recognizers=[], scale=0.4, frame_count=5, sign_in=False):
        self.win = None
        self.recognizers = recognizers
        self.scale = scale
        self.max_frame_count = frame_count
        self.frame_count = frame_count
        self.known_face_encodings = []
        self.known_face_names = []
        self.face_locations = []
        self.face_names = []
        self.sign_in = sign_in
        self.frame = None

    def is_rec(self, name):
        for r in self.recognizers:
            if r.name == name:
                return True
        return False

    def setup(self):
        self.recognizers = []
        self.known_face_names = []
        self.known_face_encodings = []
        known_faces_list = os.listdir(Recognizer.KNOWN_FACES)
        for face_dir in known_faces_list:
            self.recognizers.append(Recognizer(face_dir))
            self.known_face_names.append(face_dir)
        for rec in self.recognizers:
            self.known_face_encodings.append(rec.get_encodings()[0])

    def add_face(self, event, x, y, flags, param):

        if event == cv2.EVENT_LBUTTONDBLCLK:
            faces_and_names, frame = self.find_and_label_faces()
            frame = self.win.get_frame()
            for (top, right, bottom, left), n in faces_and_names:
                top = int(top * (1 / self.scale))
                right = int(right * (1 / self.scale))
                bottom = int(bottom * (1 / self.scale))
                left = int(left * (1 / self.scale))
                p1 = (int(left), int(top))
                p2 = (int(right), int(bottom))
                if y > top and y < bottom and x > left and x < right:
                    img = frame.crop(p1, p2)
                    r = input("Do you wan to enter this face? (y/n): ")
                    if r.lower() == "y":
                        email = input("Email: ")
                        unique_member = email.split("@")[0]
                        os.makedirs(os.path.join(Recognizer.KNOWN_FACES, unique_member))
                        img.create_image(os.path.join(Recognizer.KNOWN_FACES, unique_member,
                                                      "{0}.png".format(unique_member)))
                        first_name = input("First Name: ")
                        last_name = input("Last Name: ")
                        with open('club_members.csv', mode='a+') as csv_file:
                            member_writer = csv.writer(csv_file)
                            member_writer.writerow([first_name, last_name, email])
                        self.setup()
                else:
                    pass

    def find_and_label_faces(self):
        frame = self.win.get_frame()
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = frame.scale(self.scale)
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame.to_rgb()
        # Find all the faces and face encodings in the current frame of video
        self.face_locations = face_recognition.face_locations(rgb_small_frame.img)
        face_encodings = face_recognition.face_encodings(rgb_small_frame.img, self.face_locations)

        self.face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "who dis?"

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]

            self.face_names.append(name)
        self.frame_count = 0

        return zip(self.face_locations, self.face_names), frame

    def draw_rectangle_face_box(self, point1, point2, name, color):
        # Draw a box around the face
        self.frame = self.frame.rectangle(point1, point2, color[::-1])
        self.win.update_image(self.frame)

        # Draw a label with a name below the face
        cv2.rectangle(self.frame.img, (point1[0], point2[1] - 35), (point2[0], point2[1]), color[::-1], cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(self.frame.img, name, (point1[0] + 6, point2[1] - 6), font, 1.0, (255, 255, 255), 1)

    def draw_and_get_rectangles(self):
        self.frame = self.win.get_frame()
        color = ()
        for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            p1 = (int(left/self.scale), int(top/self.scale))
            p2 = (int(right/self.scale), int(bottom/self.scale))
            if self.green_condition(name):
                color = (0, 255, 0)
            else:
                color = (255, 0, 0)
            self.draw_rectangle_face_box(p1, p2, name, color)

    def start_window(self, update=True):
        self.win = Window('Recognize', video=True)
        self.win.mouse_event(self.add_face)
        if update:
            while not self.win.closed:
                if self.frame_count == self.max_frame_count:
                    self.find_and_label_faces()
                    self.frame_count = 0
                self.draw_and_get_rectangles()
                self.win.update_image(self.frame)
                if self.win.close_after_key(27):
                    break
                self.frame_count += 1

    def green_condition(self, name):
        return False


def recognize(process_frame_count=2):
   r = RecognizeFaces(frame_count=process_frame_count)
   r.setup()
   r.start_window()




