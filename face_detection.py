import cv2
from faceTraining import FaceTraining

class FaceDetection:
    def __init__(self):
        # Encode faces from a folder
        self.sfr = FaceTraining()
        self.sfr.load_encoding_images("image/")

        # Load Camera
        self.cap = cv2.VideoCapture(0)


    # Function to Detect Faces
    def detect_images(self,frame):
        # Detect Faces
        face_locations, face_names = self.sfr.detect_known_faces(frame)
        for face_loc, name in zip(face_locations, face_names):
            top, right, bottom, left = face_loc
            
            # Draw a rectangle around a face with person name above rectangle 
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 200), 4)

        key = cv2.waitKey(1)

cv2.destroyAllWindows()