
# Employee Monitoring System

Nowadays, many companies are using a stop and wait attendance system to mark the attendance of the employees in a company which includes either an app to mark the attendance when the employee comes in the office premise or their is a system which scans the face of the employee for which employee needs to wait and mark the attendance. Sometimes, if a bunch of employees come at a time, then these employees need to wait to mark their attendance which takes a minimum of 5 to 10 minutes. When it comes to a company's point of view, then these 5 to 10 minutes or more of each employee can be a trot to the company. What if these 5 to 10 minutes of each employee in the worst case can be saved. So to address the above problem, the software named as Employee Monitoring System can be game changing for companies which provides the real time employee monitoring feature reducing 5 to 10 minutes of employees time. The employee need not have to wait to mark the attendance. As the employee is moving towards the entrance gate, the software through the camera attached over the entrance gate will automatically catch the employee's face and the attendance will be marked for that day.



## Features


- Live detection preview
- Intuitive UI & realtime user-friendly dashboard
- Data accessibility through Google Sheets
- Efficient data filtering search functions based on the users preference
- Improved attendance processes, eliminating 5 to 10   minutes of unnecessary waiting time per employee
- If a employee goes inside the office and comes back outside and then again goes in the office, then that employee attendance will be marked only once if the employee does this activity within 10 minutes of first attendance mark. This 10 minutes of duration is customizable based on the companies requirement.



## Tech Stack

#### Python, Sqlite, Opencv, PyQt, Linux, Vscode

[![My Skills](https://skillicons.dev/icons?i=python,sqlite,opencv,qt,linux,visualstudio)](https://skillicons.dev)



## Working Methodology

#### Sign Up Page (Registration Page) : 

The sign-up page is a web page where our users can register themselves. This page typically contains a form where users can enter their personal information, such as their employee id, full name, email address, mobile no, permanent address, pincode, designation and a small capture window which captures the user's face.

The sign-up page requires the user to enter their mobile no that meets certain criteria, such as containing exactly 10 numbers of characters.  The users are also asked to enter the valid and correct email id.

The sign up page contains a small capture window which captures the user's face as soon as the capture button is clicked. After filling all the information and capturing the face, as soon as the user clicks on the submit button, the entire information of the user is stored in the database. 


#### Landing Page ( Home Page): 

Our website typically allows users to navigate to a sign up page or dashboard page. The Landing page typically contains a capturing section which takes the continuous feed from the camera, gets trained using computer vision algorithms, and detects whether the employee or bunch of employees face from the camera feed matches in from the database. If matched, it will draw a rectangle with the name of the person mentioned above the rectangle as well as mark the attendance of that employee or bunch of employees present in the camera feed and will update the entry of that employee of a company.



#### Dashboard Page ( Report Window): 

A dashboard web page is a result page typically a page that displays listings of employees attendance data. This page is generally for managers or the person who actively tracks the attendance and manages the leaves of the employees in a company. Apart from that, this page contains a search function that allows users to filter properties based on the preferences, such as start date - end date, name, employee id, and other features.

The design of the dashboard webpage is important, and it is visually appealing, easy to navigate. Overall, our dashboard webpage is user-friendly and provides users with the information they need to make informed decisions about their attendance search. The webpage is updated regularly to ensure that the listings are accurate and up-to-date.







## Run Locally

### Clone the project

```bash
  git clone https://github.com/tanishpophale53/Employee-Monitoring-System
```

### Go to the project directory

```bash
  cd project-name
```

### Install dependencies

```bash
  pip install -r requirements.txt
```

### Run the project

```bash
  python3 app.py
  (Make sure to use python or python3 based on the version of python installed on your system)
```


## Documentation

You can find the documentation at -
https://shorturl.at/aosD8


## FAQ

#### How to connect the sqlite data to google sheets?

One can use pygsheets library of python in order to connect the sqlite data to google sheets. 

#### How to create user interface using PyQt easily without programming?

One can easily create user interface using QT Designer software which saves the file as .ui file and can be easily used in development by just importing.

#### How to use the software?

Just download and run the exe file in order to use the software. If you want to run the software locally and see the files code, you can follow the section of Run Locally mentioned above.

#### What if I want to deploy the software in Raspberry PI5?

Raspberry PI5 has a great ability to process computer vision functionalities smoothly. So, one needs to just download the requirements.txt file in Raspberry PI5 and run the project files. It will successfully run. If you want to run the software on start up of Raspberry PI5, one can make service file or .sh file.
Please make sure to properly download the libraries otherwise it will cause error while running the software.


## Appendix

Reference to connect your sqlite database to google sheets - 
https://medium.com/learning-sql/how-to-use-a-google-spreadsheet-as-a-database-3c6f85eea78e







## Feedback

If you have any feedback, please reach out to me at tanishpophale@gmail.com

