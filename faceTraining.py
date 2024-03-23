import face_recognition
import cv2
import os
import glob
import numpy as np
from datetime import datetime, timedelta
from reportwindow import ReportWindow
from database import DataBase


class FaceTraining:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        
        # Call Database Class
        self.database = DataBase()

        # Resize frame for a faster speed
        self.frame_resizing = 0.35

        # Call create table function from database if it doesnot exists
        self.database.create_table()

        # Call ReportWindow Class
        self.report_window = ReportWindow()


    # Function to load encoding images
    def load_encoding_images(self, images_path):
        """
        Function Working-
        Load encoding images from path
        :param images_path:
        :return:
        """
        # Load Images
        images_path = glob.glob(os.path.join(images_path, "*.*"))

        print("{} encoding images found.".format(len(images_path)))

        # Store image encoding and names
        for img_path in images_path:
            img = cv2.imread(img_path)
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Get the filename only from the initial file path.
            basename = os.path.basename(img_path)
            (filename, ext) = os.path.splitext(basename)
            # Get encoding
            img_encoding = face_recognition.face_encodings(rgb_img)[0]

            # Store file name and file encoding
            self.known_face_encodings.append(img_encoding)
            self.known_face_names.append(filename)
        print("Encoding images loaded")


    # Function to detect known faces
    def detect_known_faces(self, frame):
        small_frame = cv2.resize(frame, (0, 0), fx=self.frame_resizing, fy=self.frame_resizing)
        # Find all the faces and face encodings in the current frame of video
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"

            # use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]

                current_time = datetime.now()
                last_10_minutes = current_time - timedelta(minutes=10)
                
                user_data = self.database.get_user_data(name)
                print(user_data)
                if user_data:
                    Companyid, Timestamp, FullName, Email, MobileNo, Address, PinCode, State, Designation = user_data
                    last_detection = self.get_last_detection(Companyid, last_10_minutes)

                    if not last_detection:
                        self.database.store_detected_data(Companyid, current_time, *user_data[2:])
                        self.report_window.update_report()
                        self.database.update_google_sheet()
                
            face_names.append(name)

        # Convert to numpy array to adjust coordinates with frame resizing quickly
        face_locations = np.array(face_locations)
        face_locations = face_locations / self.frame_resizing
        return face_locations.astype(int), face_names

    
    # Function to get the last detection
    def get_last_detection(self, company_id, last_10_minutes):
        detected_data = self.database.get_detected_faces_data()
        for data in detected_data:
            data_timestamp = datetime.strptime(data[1], "%Y-%m-%d %H:%M:%S")
            if data[0] == company_id and data_timestamp >= last_10_minutes:
                return True
        return False
    