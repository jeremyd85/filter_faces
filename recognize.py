import face_recognition
import os
from cv_window import Window
from cv_image import Image
import cv2
import numpy as np


class Recognizer:

    KNOWN_FACES = 'known_faces'

    def __init__(self, name, max_images=10):
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


def recognize(process_frame_count=2):
    scale = .40
    frame_count = process_frame_count
    known_face_encodings = []
    recognizers = []
    known_face_names = []
    known_faces_list = os.listdir(Recognizer.KNOWN_FACES)
    for face_dir in known_faces_list:
        recognizers.append(Recognizer(face_dir))
        known_face_names.append(face_dir)
    for rec in recognizers:
        known_face_encodings.append(rec.get_encodings()[0])

    win = Window('Recognize', video=True)
    while not win.closed:
        frame = win.get_frame()
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = frame.scale(scale)
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame.to_rgb()

        # Only process every other frame of video to save time
        if frame_count == process_frame_count:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame.img)
            face_encodings = face_recognition.face_encodings(rgb_small_frame.img, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "who dis?"

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)
            frame_count = 0

        frame_count += 1

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top = int(top * 1/scale)
            right = int(right * 1/scale)
            bottom = int(bottom * 1/scale)
            left = int(left * 1/scale)
            p1 = (int(left), int(top))
            p2 = (int(right), int(bottom))
            # Draw a box around the face
            frame = frame.rectangle(p1, p2)

            # Draw a label with a name below the face
            cv2.rectangle(frame.img, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame.img, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        win.update_image(frame)
        if win.close_after_key(27):
            break




