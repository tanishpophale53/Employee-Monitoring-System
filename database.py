import sqlite3
from datetime import datetime
import pygsheets

class DataBase:

    # Function to Create DataBase and Table if it doesnot exists
    def create_table(self):
        conn = sqlite3.connect('form_data.db')
        cursor = conn.cursor()

        # Create FormData table if not exists
        cursor.execute('''CREATE TABLE IF NOT EXISTS FormData
                        (Companyid TEXT , FullName TEXT, Email TEXT, MobileNo TEXT,
                        Address TEXT, PinCode TEXT, State TEXT, Designation TEXT,
                        Timestamp DATETIME)''')

        # Create DetectedFacesData table if not exists
        cursor.execute('''CREATE TABLE IF NOT EXISTS DetectedFacesData
                        (Companyid TEXT , FullName TEXT, Email TEXT, MobileNo TEXT,
                        Address TEXT, PinCode TEXT, State TEXT, Designation TEXT,
                        Timestamp DATETIME)''')

        conn.commit()
        conn.close()


    # Function to Store Registration Data
    def store_data(self, Companyid, fullname, email, mobno, address, pincode, state, designation):
        conn = sqlite3.connect('form_data.db')
        cursor = conn.cursor()

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get current timestamp
        
        cursor.execute("INSERT INTO FormData (Timestamp, Companyid, FullName, Email, MobileNo, Address, PinCode, State, Designation) \
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (timestamp, Companyid, fullname, email, mobno, address, pincode, state, designation))

        conn.commit()
        conn.close()


    # Function to Store Detected Persons Data in DetectedFacesData table
    def store_detected_data(self, Companyid, timestamp, fullname, email, mobno, address, pincode, state, designation):
        conn = sqlite3.connect('form_data.db')
        cursor = conn.cursor()

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get current timestamp

        
        cursor.execute("INSERT INTO DetectedFacesData (Companyid, Timestamp,FullName, Email, MobileNo, Address, PinCode, State, Designation) \
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (Companyid, timestamp, fullname, email, mobno, address, pincode, state, designation))

        conn.commit()
        conn.close()


    # Function to Get Registration Data from FormData table
    def get_registration_data(self):
        conn = sqlite3.connect('form_data.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM FormData")
        data = cursor.fetchall()

        conn.close()
        return data


    # Function to get particular user data
    def get_user_data(self,name):
        conn = sqlite3.connect('form_data.db')
        cursor = conn.cursor()

        cursor.execute("SELECT Companyid, Timestamp, FullName, Email, MobileNo, Address, PinCode, State, Designation FROM FormData WHERE FullName = ?", (name,))
        data = cursor.fetchone()

        conn.close()
        return data


    # Function to get Detected Persons data 
    def get_detected_faces_data(self):
        conn = sqlite3.connect('form_data.db')
        cursor = conn.cursor()

        cursor.execute("SELECT Companyid, Timestamp, FullName, Email, MobileNo, Designation, Address, PinCode, State FROM DetectedFacesData")
        data = cursor.fetchall()

        conn.close()
        return data


    # Function to update Google Sheet with SQLite data
    def update_google_sheet(self):
        # Connect to SQLite database and fetch data
        detected_faces_data = self.get_detected_faces_data()

        # Convert the retrieved data into the correct format for insertion
        rows_to_insert = []
        for row in detected_faces_data:
            # Convert each row from the SQLite data into a list (adjust column indexes accordingly)
            formatted_row = [
                row[0],  # Column 1 data
                row[1],  # Column 2 data
                row[2],  # Column 3 data
                row[3],  # Column 4 data
                row[4],  # Column 5 data
                row[5],  # Column 6 data
                row[6],  # Column 7 data
                row[7],  # Column 8 data
                row[8],  # Column 9 data
             ]
            rows_to_insert.append(formatted_row)

        # Authorize and open the Google Sheet
        gc = pygsheets.authorize(service_file='medium-sample-project-413112-e0a77af4d3a2.json')  # Replace with your credentials file path
        sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1Sbh8eqnlhMSHHurahLDeldxN38bhjhH00QO1QrfQe9g/edit#gid=0")  # Replace with your Sheet URL
        sheet = sh.sheet1  # Select the desired sheet
        
        # Clear existing data in the sheet
        sheet.clear()

        # Update Google Sheet with data from SQLite
        sheet.insert_rows(row=1, values=rows_to_insert)

