import sys
import cv2
import re
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLabel
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer, Qt
from PyQt5.uic import loadUi
from database import DataBase


class RegistrationWindow(QMainWindow):
    def __init__(self):
        super(RegistrationWindow, self).__init__()

        self.database = DataBase()

        #Load the Registration UI File
        loadUi('registration.ui', self) 

        # Initialize the Camera
        self.init_camera()
        
        # Captured image during registration
        self.captured_image = None       
        self.capture_count = 0

        # Input Field PlaceHolder Text
        self.companyIDLineInput.setPlaceholderText('Enter your Company ID')
        self.fullNameLineInput.setPlaceholderText('Ex - Rahul Sahu')
        self.emailIDLineInput.setPlaceholderText('Enter your email address')
        self.mobileNoLineInput.setPlaceholderText('Enter 10 Digit Mobile No')
        self.addressLineInput.setPlaceholderText('Enter your address')
        self.pinCodeInput.setPlaceholderText('Enter your Pincode')
        self.stateLineInput.setPlaceholderText('Full Name of your State')
        self.designationLineInput.setPlaceholderText('Enter your Designation')
    
        # Input Fileds Border template
        self.companyIDLineInput.setStyleSheet("border: 1px solid black;")
        self.fullNameLineInput.setStyleSheet("border: 1px solid black;")
        self.emailIDLineInput.setStyleSheet("border: 1px solid black;")
        self.mobileNoLineInput.setStyleSheet("border: 1px solid black;")
        self.addressLineInput.setStyleSheet("border: 1px solid black;")
        self.pinCodeInput.setStyleSheet("border: 1px solid black;")
        self.stateLineInput.setStyleSheet("border: 1px solid black;")
        self.designationLineInput.setStyleSheet("border: 1px solid black;")
        
        # Connect input fields to enable/disable the submit button
        self.companyIDLineInput.textChanged.connect(self.check_submit_enable)
        self.fullNameLineInput.textChanged.connect(self.check_submit_enable)
        self.emailIDLineInput.textChanged.connect(self.check_submit_enable)
        self.mobileNoLineInput.textChanged.connect(self.check_submit_enable)
        self.addressLineInput.textChanged.connect(self.check_submit_enable)
        self.pinCodeInput.textChanged.connect(self.check_submit_enable)
        self.stateLineInput.textChanged.connect(self.check_submit_enable)
        self.designationLineInput.textChanged.connect(self.check_submit_enable)

        # When the Capture button is pressed execute capture_image function
        self.CaptureButton.clicked.connect(self.capture_image)

        # When the Submit button is pressed execute store_data function
        self.SubmitButton.clicked.connect(self.store_data)

        #Initially set Submit button to False or Disabled
        self.SubmitButton.setEnabled(False)

        # Create the database table if not exists
        self.database.create_table()  

        # Add a QLabel for the background image
        self.backgroundLabel = QLabel(self)
        self.backgroundLabel.setGeometry(0, 0, self.width(), self.height())
        self.backgroundLabel.setScaledContents(True)

        # Set the background image
        background_pixmap = QPixmap('WindowsBackgroundImage.jpg')
        self.backgroundLabel.setPixmap(background_pixmap)

        # Ensure the background stays behind other widgets
        self.backgroundLabel.lower()


    # Initiate Camera
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


    # Detect the frame and Display
    def detect_and_display(self):
        ret, frame = self.camera.read()
        if ret:
            Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            FlippedImage = cv2.flip(Image, 1)
            ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format_RGB888)
            Pic = ConvertToQtFormat.scaled(400, 240, Qt.KeepAspectRatio)
            self.CaptureFrame.setPixmap(QPixmap.fromImage(Pic))
            self.CaptureFrame.setScaledContents(True)  # Make the label's pixmap scaled


    # Function to resize the background label based on change of size of registration-window in realtime
    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Update the size of the background label based on the window's new size
        self.backgroundLabel.setGeometry(0, 0, self.width(), self.height())


    #Capture the image from the frame
    def capture_image(self):
        if self.capture_count < 2:
            ret, frame = self.camera.read()

            # Save the full frame
            self.captured_image = frame  
            self.capture_count += 1

            if self.capture_count == 1:
                self.SubmitButton.setEnabled(True)
                self.CaptureButton.setEnabled(False)
        else:
            self.CaptureButton.setEnabled(False)

  
    # Validate Email 
    def validate_email(self, email):
        # Email validation regex pattern
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(pattern, email)


    # Validate MobNo
    def validate_mobno(self, mobno):
        return len(mobno) == 10 and mobno.isdigit()


    # Validate all registration fields
    def validate_fields(self):
        mandatory_fields = [
            self.companyIDLineInput.text(),
            self.fullNameLineInput.text(),
            self.emailIDLineInput.text(),
            self.mobileNoLineInput.text(),
            self.addressLineInput.text(),
            self.pinCodeInput.text(),
            self.stateLineInput.text(),
            self.designationLineInput.text()
        ]

        email = self.emailIDLineInput.text()
        mobno = self.mobileNoLineInput.text()

        # Validate email
        if not self.validate_email(email):
            QMessageBox.warning(self, "Warning", "Please enter a valid email.")
            return False

        # Validate mobile number length
        if not self.validate_mobno(mobno):
            QMessageBox.warning(self, "Warning", "Please enter a 10-digit Mobile Number.")
            return False

        return True
    
    
    # Check whether all fields are field or not
    def check_submit_enable(self):
        # Enable the submit button only when all fields are filled and images are captured
        if (
            all([
                self.companyIDLineInput.text(),
                self.fullNameLineInput.text(),
                self.emailIDLineInput.text(),
                self.mobileNoLineInput.text(),
                self.addressLineInput.text(),
                self.pinCodeInput.text(),
                self.stateLineInput.text(),
                self.designationLineInput.text(),
            ])
        ):
            self.SubmitButton.setEnabled(True)
        else:
            self.SubmitButton.setEnabled(False)

    
    # Store data in the database after clicking on submit button
    def store_data(self):
        if not self.validate_fields():
            return

        companyid = self.companyIDLineInput.text() 
        fullname = self.fullNameLineInput.text()
        email = self.emailIDLineInput.text()
        mobno = self.mobileNoLineInput.text()
        address = self.addressLineInput.text()
        pincode = self.pinCodeInput.text()
        state = self.stateLineInput.text()
        designation = self.designationLineInput.text()

        # Save the captured image to the "image" folder
        image_folder_path = "image"
        if not os.path.exists(image_folder_path):
            os.makedirs(image_folder_path)

        image_path = os.path.join(image_folder_path, f"{fullname}.jpg")
        cv2.imwrite(image_path, self.captured_image)
        
        # Release camera access
        self.close()

        QMessageBox.information(self, "Information", "Data stored successfully.")
        self.database.store_data(companyid, fullname, email, mobno, address, pincode, state, designation)
    
        # Open main window - when submit button is pressed registration window closes and main window opens
        from mainwindow import MyMainWindow
        self.main_window = MyMainWindow()
        self.main_window.show()
    

    # Close method to release the camera even if the window is closed
    def close(self):
        self.camera.release()
        super(RegistrationWindow, self).close()


