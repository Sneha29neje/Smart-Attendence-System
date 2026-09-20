# Smart Attendance System - Flask + MongoDB Atlas

This version uses MongoDB for students, faculty, and attendance. The old SQLite `attendance.db` file is not used.

## Collections

Database: `smart_attendance`

- `students`
- `faculty`
- `attendance`

## Run on Windows PowerShell

```powershell
python -m venv test
.\test\Scripts\Activate.ps1
pip install -r requirements.txt
$env:MONGO_URI="YOUR_REAL_MONGODB_ATLAS_CONNECTION_STRING"
python app.py
```

Open `http://127.0.0.1:5000`.

## MongoDB Atlas

Create a database user and use its exact username/password in the connection string. In Atlas Network Access, add your current IP address. If authentication fails, reset the database user's password and generate a fresh connection string.

Do not commit the real MongoDB URI/password to GitHub.
