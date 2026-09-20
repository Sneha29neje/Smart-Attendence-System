# Smart Attendance System - Flask + MongoDB Atlas

## 📌 Project Overview

The **Smart Attendance System** is a web-based attendance management application developed using **Python Flask** and **MongoDB Atlas**.

The system is designed to make student attendance management easier, faster, and more organized. Instead of maintaining attendance records manually, faculty members can use the web application to manage students, maintain faculty information, and record daily attendance digitally.

The application uses **MongoDB Atlas** as the cloud database. Student details, faculty information, and attendance records are stored in separate MongoDB collections.

---

## 🎯 Objectives

The main objectives of the Smart Attendance System are:

* To digitize the traditional attendance process.
* To reduce manual attendance work.
* To maintain student information in an organized manner.
* To allow faculty to record daily attendance.
* To store attendance records securely in a database.
* To provide an easy-to-use web interface.
* To make attendance data easier to manage and retrieve.
* To use a cloud-based MongoDB database for storing application data.

---

## ✨ Features

### 👨‍🎓 Student Management

* Add student details.
* Store student information in MongoDB.
* View registered students.
* Maintain student records in an organized manner.

### 👩‍🏫 Faculty Management

* Store faculty information.
* Manage faculty records.
* Associate attendance activities with faculty members.

### 📋 Attendance Management

* Select an attendance date.
* Display registered students.
* Mark students as **Present** or **Absent**.
* Store attendance records in MongoDB.
* Retrieve attendance information when required.

### 🗄️ Database Management

The application uses **MongoDB Atlas** as its database.

Database name:

```text
smart_attendance
```

Collections:

```text
students
faculty
attendance
```

---

## 🛠️ Technologies Used

| Technology                 | Purpose                       |
| -------------------------- | ----------------------------- |
| Python                     | Backend programming           |
| Flask                      | Web application framework     |
| MongoDB Atlas              | Cloud database                |
| HTML5                      | Web page structure            |
| CSS3                       | Styling and layout            |
| Jinja2                     | Dynamic HTML templates        |
| PyMongo                    | MongoDB connectivity          |
| Python Virtual Environment | Project dependency management |

---

## 🏗️ System Architecture

The project follows a simple web application architecture:

```text
User / Faculty
      ↓
Web Browser
      ↓
HTML + CSS + Jinja2
      ↓
Flask Application
      ↓
PyMongo
      ↓
MongoDB Atlas
      ↓
smart_attendance Database
      ├── students
      ├── faculty
      └── attendance
```

---

## 📂 Database Structure

### Database

```text
smart_attendance
```

### 1. Students Collection

The `students` collection stores student information.

Example information:

```text
student ID
name
roll number
class/course
other student details
```

### 2. Faculty Collection

The `faculty` collection stores faculty-related information.

Example information:

```text
faculty ID
name
email
department
other faculty details
```

### 3. Attendance Collection

The `attendance` collection stores attendance information.

Example information:

```text
student
date
attendance status
faculty
```

---

## 📁 Project Structure

A typical project structure is:

```text
smart_attendance_system/
│
├── app.py
├── requirements.txt
├── README.md
│
├── templates/
│   ├── index.html
│   ├── ...
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
└── test/
    ├── Scripts/
    └── ...
```

> The exact files and folders may vary depending on the final version of the project.

---

## ⚙️ Installation and Setup

### Step 1: Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Move into the project directory:

```bash
cd smart_attendance_system
```

---

### Step 2: Create a Virtual Environment

On Windows PowerShell:

```powershell
python -m venv test
```

Activate the virtual environment:

```powershell
.\test\Scripts\Activate.ps1
```

---

### Step 3: Install Dependencies

```powershell
pip install -r requirements.txt
```

---

## ☁️ MongoDB Atlas Configuration

This project uses **MongoDB Atlas** instead of the old SQLite database.

Create a MongoDB Atlas cluster and create a database user.

The application expects a MongoDB connection string through the `MONGO_URI` environment variable.

On Windows PowerShell:

```powershell
$env:MONGO_URI="YOUR_REAL_MONGODB_ATLAS_CONNECTION_STRING"
```

Then run:

```powershell
python app.py
```

Open the application in your browser:

```text
http://127.0.0.1:5000
```

---

## 🔐 Security

**Never upload your real MongoDB username, password, or connection string to GitHub.**

Do not write this directly in your source code:

```python
MONGO_URI = "mongodb+srv://username:password@..."
```

Instead, use an environment variable:

```python
import os

MONGO_URI = os.environ.get("MONGO_URI")
```

You should also add sensitive files such as `.env` to `.gitignore` if you use them.

Example:

```text
.env
test/
__pycache__/
*.pyc
```

If a MongoDB password or connection string is accidentally uploaded to GitHub, change the database user's password immediately and create a new connection string.

---

## ▶️ Running the Application

After activating the virtual environment and configuring MongoDB Atlas:

```powershell
python app.py
```

The Flask development server will start.

Open:

```text
http://127.0.0.1:5000
```

in your browser.

---

## 🔄 Application Workflow

The basic workflow of the system is:

```text
Start Application
       ↓
Connect to MongoDB Atlas
       ↓
Load Student Records
       ↓
Select Attendance Date
       ↓
Display Students
       ↓
Mark Present / Absent
       ↓
Submit Attendance
       ↓
Store Attendance in MongoDB
       ↓
Attendance Record Saved
```

---

## 📊 Advantages

* Reduces manual attendance work.
* Saves attendance data digitally.
* Provides centralized data storage.
* Uses MongoDB Atlas cloud database.
* Easy to maintain and update.
* Reduces the possibility of losing paper attendance records.
* Provides a simple interface for faculty.
* Can be extended with additional features in the future.

---

## 🚀 Future Enhancements

The project can be further improved by adding:

* Faculty login and authentication.
* Student login.
* Admin dashboard.
* Attendance percentage calculation.
* Monthly and weekly attendance reports.
* Search and filter functionality.
* Export attendance to Excel or PDF.
* Email notifications for low attendance.
* Dashboard with attendance statistics.
* Role-based access control.
* Face-recognition-based attendance.
* QR-code-based attendance.
* Improved mobile-responsive design.

---

## 🧪 Testing

The application can be tested by performing the following operations:

1. Start the Flask application.
2. Connect the application to MongoDB Atlas.
3. Add student records.
4. Add faculty records.
5. Select an attendance date.
6. Mark students as Present or Absent.
7. Submit the attendance.
8. Verify that the attendance record is stored in MongoDB Atlas.
9. Retrieve and verify attendance information.

---

## 📸 Screenshots

Screenshots of the application can be added here to demonstrate the user interface.

### Home Page

*Add screenshot here*

### Student Management

*Add screenshot here*

### Faculty Management

*Add screenshot here*

### Mark Attendance

*Add screenshot here*

### Attendance Records

*Add screenshot here*

### MongoDB Atlas Database

*Add screenshot here*

---

## 🎓 Learning Outcomes

Through this project, I gained practical experience in:

* Python programming
* Flask web development
* MongoDB database management
* MongoDB Atlas cloud database
* CRUD operations
* Jinja2 templates
* HTML and CSS
* Backend development
* Database connectivity
* Environment variables
* Virtual environments
* Basic web application architecture

---

## 📌 Project Status

**Status:** Completed / In Development

The current version provides a basic web-based attendance management system using **Flask and MongoDB Atlas**. Additional features can be added in future versions.

---

## 👩‍💻 Author

**Sneha**

This project was developed as a learning project to gain practical experience in **Python Flask, backend development, and MongoDB database management**.
