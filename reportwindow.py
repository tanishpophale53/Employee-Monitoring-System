from PyQt5.QtWidgets import (
    QSizePolicy, QTableWidget, QMainWindow, QTableWidgetItem, QWidget, QLabel, QLineEdit, 
    QPushButton, QHBoxLayout, QHeaderView, QGridLayout, QApplication
)
from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont, QPixmap
from datetime import datetime, timedelta
from database import DataBase
import pandas as pd


class ReportWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Call Database class
        self.database = DataBase()
    
        # Report Window Title and Geometry
        self.setWindowTitle("Employee Monitoring System - Dashboard")
        
        # Set initial size to the screen size
        screen_size = QApplication.desktop().screenGeometry()
        self.resize(screen_size.width(), screen_size.height()-71)
        
        # Add a QLabel for the background image
        self.backgroundLabel = QLabel(self)
        self.backgroundLabel.setGeometry(0, 0, self.width(), self.height())
        self.backgroundLabel.setScaledContents(True)

        # Set the background image
        background_pixmap = QPixmap('WindowsBackgroundImage.jpg')
        self.backgroundLabel.setPixmap(background_pixmap)

        # Ensure the background stays behind other widgets
        self.backgroundLabel.lower()

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Set the size policy for the central widget
        self.central_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.layout = QGridLayout(self.central_widget)

        # Filter by Name or Company ID
        self.filter_label = QLabel("Filter by Name or Company ID:")
        self.filter_label.setStyleSheet("QLabel{font-size: 10pt; font-weight: bold; font-family: Arial;}")
        self.layout.addWidget(self.filter_label, 0, 0, 1, 1)  # Row 0, Col 0, Span 1 row, 1 column

        self.filter_input = QLineEdit()
        self.layout.addWidget(self.filter_input, 0, 1, 1, 1)  # Row 0, Col 1, Span 1 row, 1 column

        # Date Range Filter
        self.date_range_label = QLabel("Filter by Date Range (YYYY-MM-DD):")
        self.date_range_label.setStyleSheet("QLabel{font-size: 10pt; font-weight: bold; font-family: Arial;}")
        self.layout.addWidget(self.date_range_label, 1, 0, 1, 1)  # Row 1, Col 0, Span 1 row, 1 column

        self.date_range_layout = QHBoxLayout()
        self.layout.addLayout(self.date_range_layout, 1, 1, 1, 1)  # Row 1, Col 1, Span 1 row, 1 column

        self.start_date_input = QLineEdit()
        self.start_date_input.setPlaceholderText("Start Date")
        self.start_date_input.setStyleSheet("QLabel{font-size: 15pt; font-weight: bold;}")
        self.date_range_layout.addWidget(self.start_date_input)
        
        # End Date Filter Display
        self.end_date_input = QLineEdit()
        self.end_date_input.setPlaceholderText("End Date (End date isn't being included in results)")
        self.end_date_input.setStyleSheet("QLabel{font-size: 15pt; font-weight: bold;}")
        self.date_range_layout.addWidget(self.end_date_input)

        self.filter_button = QPushButton("Filter")
        self.filter_button.setStyleSheet("QPushButton{font-size: 10pt;  font-weight: bold; font-family: Arial;}")
        self.filter_button.clicked.connect(self.filter_data)
        self.layout.addWidget(self.filter_button, 2, 0, 1, 2)  # Row 2, Col 0, Span 1 row, 2 columns

        self.export_button = QPushButton("Export as Excel")
        self.export_button.setStyleSheet("QPushButton{font-size: 10pt;  font-weight: bold; font-family: Arial;}")
        self.export_button.clicked.connect(self.export_as_excel)
        self.layout.addWidget(self.export_button, 3, 0, 1, 2)  # Row 3, Col 0, Span 1 row, 2 columns

        self.table_widget = QTableWidget()
        self.layout.addWidget(self.table_widget, 4, 0, 1, 2)  # Row 4, Col 0, Span 1 row, 2 columns

        # Set the size policy for the table widget
        self.table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # Stretch columns to fill the available space

        # Set the layout stretch for the central widget
        self.layout.setColumnStretch(0, 1)  # Stretch the first column
        self.layout.setColumnStretch(1, 2)  # Stretch the second column

        self.update_report()

  
    # Function to resize the background label based on change of size of report-window in realtime
    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Update the size of the background label based on the window's new size
        self.backgroundLabel.setGeometry(0, 0, self.width(), self.height())


    # Function to update report
    def update_report(self):
        # Call Detected Faces Data function from Database Class
        detected_faces_data = self.database.get_detected_faces_data()
        print(detected_faces_data)

        self.original_data = detected_faces_data  # Store original data for filtering

        self.table_widget.setRowCount(len(detected_faces_data))

        column_labels = ["Companyid", "TimeStamp", "Name", "Email", "Mobile No", "Designation", "Address", "PinCode", "State"]  # Modify as per your data

        self.table_widget.setColumnCount(len(column_labels))
        self.table_widget.setHorizontalHeaderLabels(column_labels)

        for col in range(self.table_widget.columnCount()):
            header_item = self.table_widget.horizontalHeaderItem(col)
            header_font = QFont("Arial", 10, QFont.Bold)  # Set font to bold
            header_item.setFont(header_font)

        # Populate table with data
        for row, data in enumerate(detected_faces_data):
            for col, value in enumerate(data):
                item = QTableWidgetItem(str(value))
                self.table_widget.setItem(row, col, item)


    # Function to Filter Data
    def filter_data(self):
        filter_text = self.filter_input.text().lower()
        start_date_text = self.start_date_input.text()
        end_date_text = self.end_date_input.text()

        # Convert start and end date strings to datetime objects
        try:
            start_date = datetime.strptime(start_date_text, "%Y-%m-%d") if start_date_text else None
            end_date = datetime.strptime(end_date_text, "%Y-%m-%d") if end_date_text else None
        except ValueError:
            # Handle invalid date format if needed
            return

        filtered_data = []

        for row in self.original_data:
            # Check if filter_text is present in any cell of the row
            contains_filter_text = any(filter_text in str(cell).lower() for cell in row)

            # Check if the timestamp is within the specified date range
            within_date_range = True
            if start_date is not None and end_date is not None:
                timestamp = datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")
                within_date_range = start_date <= timestamp <= end_date
            elif start_date is not None:
                timestamp = datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")
                within_date_range = start_date <= timestamp
            elif end_date is not None:
                timestamp = datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")
                within_date_range = timestamp <= end_date + timedelta(days=1)  # Include entries on the end date

            # Add the row to filtered_data if it satisfies both conditions
            if contains_filter_text and within_date_range:
                filtered_data.append(row)

        self.table_widget.setRowCount(len(filtered_data))

        for row, data in enumerate(filtered_data):
            for col, value in enumerate(data):
                item = QTableWidgetItem(str(value))
                self.table_widget.setItem(row, col, item)

        self.table_widget.resizeColumnsToContents()


    # Function to export table data as Excel
    def export_as_excel(self):
        # Get current table data
        export_data = []
        for row in range(self.table_widget.rowCount()):
            row_data = []
            for col in range(self.table_widget.columnCount()):
                item = self.table_widget.item(row, col)
                row_data.append(item.text() if item is not None else "")
            export_data.append(row_data)

        # Convert data to a Pandas DataFrame
        df = pd.DataFrame(export_data, columns=["Companyid", "TimeStamp", "Name", "Email", "Mobile No", "Designation", "Address", "PinCode", "State"])

        # Save DataFrame to an Excel file
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Excel File", "", "Excel Files (*.xlsx)")
        if file_path:
            df.to_excel(file_path, index=False)

