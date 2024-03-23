import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QLabel
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer, Qt
from PyQt5.uic import loadUi
from registration import RegistrationWindow
from face_detection import FaceDetection
from reportwindow import ReportWindow


class MyMainWindow(QMainWindow):
    def __init__(self):
        super(MyMainWindow, self).__init__()

        #Load the UI File
        loadUi('home.ui', self)

        # Initialize Camera  
        self.init_camera()

        # Set initial size to the screen size
        screen_size = QApplication.desktop().screenGeometry()
        self.resize(screen_size.width(), screen_size.height()-71)

        # Call FaceDetection class
        self.faceDetection = FaceDetection()

        # Add a QLabel for the background image
        self.backgroundLabel = QLabel(self)
        self.backgroundLabel.setGeometry(0, 0, self.width(), self.height())
        self.backgroundLabel.setScaledContents(True)

        # Set the background image
        background_pixmap = QPixmap('WindowsBackgroundImage.jpg')
        self.backgroundLabel.setPixmap(background_pixmap)

        # Ensure the background stays behind other widgets
        self.backgroundLabel.lower()
 
        # Connect to Registration Window
        registration_action = QAction('Registration', self)
        registration_action.triggered.connect(self.openRegistrationWindow)
        self.Registration.addAction(registration_action)

        # Connect to Report Window
        report_action = QAction('Report', self)
        report_action.triggered.connect(self.openReportWindow)
        self.Report.addAction(report_action)


    # Function to Initialize Camera
    def init_camera(self):
        self.camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        
        if not self.camera.isOpened():
            print("Error: Could not open camera.")
            sys.exit()

        self.timer = QTimer(self)

        # Connect the timer to the detect_and_display method
        self.timer.timeout.connect(self.detect_and_display)  

        # Start the timer to continuously display frames
        self.timer.start(1)  


    # Function to resize the background label based on change of size of mainwindow in realtime
    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Update the size of the background label based on the window's new size
        self.backgroundLabel.setGeometry(0, 0, self.width(), self.height())


    # Function to Capture, Detect and Display the frame
    def detect_and_display(self):
        ret, frame = self.camera.read()
        if ret:
            # Pass the frame to the face detector
            self.faceDetection.detect_images(frame) 
            Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            FlippedImage = cv2.flip(Image, 1)
            ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format_RGB888)
            Pic = ConvertToQtFormat.scaled(400, 240, Qt.KeepAspectRatio)
            self.FeedLabel.setPixmap(QPixmap.fromImage(Pic))
            # Make the label's pixmap scaled
            self.FeedLabel.setScaledContents(True)  


    # Function to open Registration Window
    def openRegistrationWindow(self):
        self.camera.release()
        self.registration_window = RegistrationWindow()
        self.registration_window.show()  # Show the Registration Window
        self.close()
    
    
    # Function to open Report Window
    def openReportWindow(self):
        self.camera.release()
        self.report_window = ReportWindow()
        self.report_window.show()  # Show the Report Window
        self.close()
    

