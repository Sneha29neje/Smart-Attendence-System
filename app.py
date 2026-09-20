from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import DuplicateKeyError
from bson import ObjectId
from datetime import datetime, date
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "smart-attendance-secret-key")

# =========================================================
# MONGODB ATLAS CONNECTION
# =========================================================
# Set your real MongoDB Atlas URI before starting the app.
# PowerShell example:
# $env:MONGO_URI="mongodb+srv://USERNAME:PASSWORD@YOUR-CLUSTER.mongodb.net/?retryWrites=true&w=majority"
#
# Do not put your real password in GitHub.

MONGO_URI = os.getenv("MONGO_URI", "").strip()

if not MONGO_URI:
    raise RuntimeError(
        "MONGO_URI is not set. Set your MongoDB Atlas connection string "
        "in the MONGO_URI environment variable."
    )

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=10000)
    client.admin.command("ping")
    print("MongoDB connected successfully!")
except Exception as e:
    print("MongoDB connection failed!")
    print(e)
    raise

# All application data is stored in this MongoDB database.
db = client["smart_attendance"]
students_collection = db["students"]
faculty_collection = db["faculty"]
attendance_collection = db["attendance"]

# Indexes
students_collection.create_index([("roll_no", ASCENDING)], unique=True)
faculty_collection.create_index([("name", ASCENDING)])
attendance_collection.create_index(
    [("student_id", ASCENDING), ("attendance_date", ASCENDING)],
    unique=True
)
attendance_collection.create_index([("attendance_date", DESCENDING)])


def valid_object_id(value):
    try:
        return ObjectId(value)
    except Exception:
        return None


def attendance_percentage(student_id):
    total = attendance_collection.count_documents({"student_id": student_id})
    if total == 0:
        return 0.0
    present = attendance_collection.count_documents({
        "student_id": student_id,
        "status": "Present"
    })
    return round((present / total) * 100, 2)


def student_with_percentage(student):
    data = dict(student)
    data["percentage"] = attendance_percentage(student["_id"])
    return data


# =========================================================
# DASHBOARD
# =========================================================
@app.route("/")
def dashboard():
    student_count = students_collection.count_documents({})
    faculty_count = faculty_collection.count_documents({})
    attendance_count = attendance_collection.count_documents({})

    low_count = sum(
        1 for s in students_collection.find({}, {"_id": 1})
        if attendance_percentage(s["_id"]) < 75
    )

    return render_template(
        "dashboard.html",
        student_count=student_count,
        faculty_count=faculty_count,
        attendance_count=attendance_count,
        low_count=low_count
    )


# =========================================================
# STUDENTS
# =========================================================
@app.route("/students")
def students_list():
    data = [
        student_with_percentage(s)
        for s in students_collection.find().sort("roll_no", ASCENDING)
    ]
    return render_template("students.html", students=data)


@app.route("/students/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        roll_no = request.form.get("roll_no", "").strip()
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        department = request.form.get("department", "").strip()
        semester = request.form.get("semester", "").strip()

        if not roll_no or not name:
            flash("Roll number and name are required.", "error")
            return redirect(url_for("add_student"))

        try:
            students_collection.insert_one({
                "roll_no": roll_no,
                "name": name,
                "email": email,
                "department": department,
                "semester": semester,
                "created_at": datetime.now()
            })
            flash("Student added successfully.", "success")
        except DuplicateKeyError:
            flash("A student with this roll number already exists.", "error")

        return redirect(url_for("students_list"))

    return render_template("student_form.html", student=None, mode="add")


@app.route("/students/edit/<student_id>", methods=["GET", "POST"])
def edit_student(student_id):
    oid = valid_object_id(student_id)
    if oid is None:
        flash("Invalid student ID.", "error")
        return redirect(url_for("students_list"))

    student = students_collection.find_one({"_id": oid})
    if not student:
        flash("Student not found.", "error")
        return redirect(url_for("students_list"))

    if request.method == "POST":
        roll_no = request.form.get("roll_no", "").strip()
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        department = request.form.get("department", "").strip()
        semester = request.form.get("semester", "").strip()

        if not roll_no or not name:
            flash("Roll number and name are required.", "error")
            return redirect(url_for("edit_student", student_id=student_id))

        try:
            students_collection.update_one(
                {"_id": oid},
                {"$set": {
                    "roll_no": roll_no,
                    "name": name,
                    "email": email,
                    "department": department,
                    "semester": semester,
                    "updated_at": datetime.now()
                }}
            )
            attendance_collection.update_many(
                {"student_id": oid},
                {"$set": {"roll_no": roll_no, "student_name": name}}
            )
            flash("Student updated successfully.", "success")
            return redirect(url_for("students_list"))
        except DuplicateKeyError:
            flash("A student with this roll number already exists.", "error")

    return render_template("student_form.html", student=student, mode="edit")


@app.route("/students/delete/<student_id>", methods=["POST"])
def delete_student(student_id):
    oid = valid_object_id(student_id)
    if oid is None:
        flash("Invalid student ID.", "error")
        return redirect(url_for("students_list"))

    result = students_collection.delete_one({"_id": oid})
    if result.deleted_count:
        attendance_collection.delete_many({"student_id": oid})
        flash("Student and related attendance records deleted.", "success")
    else:
        flash("Student not found.", "error")

    return redirect(url_for("students_list"))


# =========================================================
# FACULTY
# =========================================================
@app.route("/faculty")
def faculty_list():
    data = list(faculty_collection.find().sort("name", ASCENDING))
    return render_template("faculty.html", faculty=data)


@app.route("/faculty/add", methods=["GET", "POST"])
def add_faculty():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        department = request.form.get("department", "").strip()
        subject = request.form.get("subject", "").strip()

        if not name:
            flash("Faculty name is required.", "error")
            return redirect(url_for("add_faculty"))

        faculty_collection.insert_one({
            "name": name,
            "email": email,
            "department": department,
            "subject": subject,
            "created_at": datetime.now()
        })
        flash("Faculty added successfully.", "success")
        return redirect(url_for("faculty_list"))

    return render_template("faculty_form.html", member=None, mode="add")


@app.route("/faculty/edit/<faculty_id>", methods=["GET", "POST"])
def edit_faculty(faculty_id):
    oid = valid_object_id(faculty_id)
    if oid is None:
        flash("Invalid faculty ID.", "error")
        return redirect(url_for("faculty_list"))

    member = faculty_collection.find_one({"_id": oid})
    if not member:
        flash("Faculty member not found.", "error")
        return redirect(url_for("faculty_list"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        department = request.form.get("department", "").strip()
        subject = request.form.get("subject", "").strip()

        if not name:
            flash("Faculty name is required.", "error")
            return redirect(url_for("edit_faculty", faculty_id=faculty_id))

        faculty_collection.update_one(
            {"_id": oid},
            {"$set": {
                "name": name,
                "email": email,
                "department": department,
                "subject": subject,
                "updated_at": datetime.now()
            }}
        )
        flash("Faculty updated successfully.", "success")
        return redirect(url_for("faculty_list"))

    return render_template("faculty_form.html", member=member, mode="edit")


@app.route("/faculty/delete/<faculty_id>", methods=["POST"])
def delete_faculty(faculty_id):
    oid = valid_object_id(faculty_id)
    if oid is None:
        flash("Invalid faculty ID.", "error")
        return redirect(url_for("faculty_list"))

    result = faculty_collection.delete_one({"_id": oid})
    flash(
        "Faculty deleted successfully." if result.deleted_count else "Faculty member not found.",
        "success" if result.deleted_count else "error"
    )
    return redirect(url_for("faculty_list"))


# =========================================================
# MARK ATTENDANCE
# =========================================================
@app.route("/attendance/mark", methods=["GET", "POST"])
def mark_attendance():
    student_data = list(students_collection.find().sort("roll_no", ASCENDING))
    selected_date = request.args.get("attendance_date", date.today().isoformat())

    if request.method == "POST":
        attendance_date = request.form.get("attendance_date", "").strip()
        if not attendance_date:
            flash("Attendance date is required.", "error")
            return redirect(url_for("mark_attendance"))

        for student in student_data:
            status = request.form.get(f"status_{student['_id']}", "Absent")
            if status not in ("Present", "Absent"):
                continue

            attendance_collection.update_one(
                {"student_id": student["_id"], "attendance_date": attendance_date},
                {"$set": {
                    "roll_no": student.get("roll_no", ""),
                    "student_name": student.get("name", ""),
                    "status": status,
                    "updated_at": datetime.now()
                }, "$setOnInsert": {"created_at": datetime.now()}},
                upsert=True
            )

        flash("Attendance saved successfully.", "success")
        return redirect(url_for("view_attendance", selected_date=attendance_date))

    existing = attendance_collection.find({"attendance_date": selected_date})
    status_map = {str(row["student_id"]): row["status"] for row in existing}

    return render_template(
        "mark_attendance.html",
        students=student_data,
        selected_date=selected_date,
        status_map=status_map
    )


# =========================================================
# VIEW ATTENDANCE
# =========================================================
@app.route("/attendance")
def view_attendance():
    selected_date = request.args.get("selected_date", "").strip()
    query = {"attendance_date": selected_date} if selected_date else {}

    records = list(attendance_collection.find(query).sort([
        ("attendance_date", DESCENDING),
        ("roll_no", ASCENDING)
    ]))

    return render_template(
        "view_attendance.html",
        attendance=records,
        selected_date=selected_date
    )


# =========================================================
# EDIT ATTENDANCE
# =========================================================
@app.route("/attendance/edit/<attendance_id>", methods=["GET", "POST"])
def edit_attendance(attendance_id):
    oid = valid_object_id(attendance_id)
    if oid is None:
        flash("Invalid attendance ID.", "error")
        return redirect(url_for("view_attendance"))

    record = attendance_collection.find_one({"_id": oid})
    if not record:
        flash("Attendance record not found.", "error")
        return redirect(url_for("view_attendance"))

    if request.method == "POST":
        attendance_date = request.form.get("attendance_date", "").strip()
        status = request.form.get("status", "").strip()

        if not attendance_date or status not in ("Present", "Absent"):
            flash("Valid date and status are required.", "error")
            return redirect(url_for("edit_attendance", attendance_id=attendance_id))

        try:
            attendance_collection.update_one(
                {"_id": oid},
                {"$set": {
                    "attendance_date": attendance_date,
                    "status": status,
                    "updated_at": datetime.now()
                }}
            )
            flash("Attendance updated successfully.", "success")
            return redirect(url_for("view_attendance"))
        except DuplicateKeyError:
            flash("This student already has attendance for that date.", "error")

    return render_template("attendance_form.html", record=record)


# =========================================================
# DELETE ATTENDANCE
# =========================================================
@app.route("/attendance/delete/<attendance_id>", methods=["POST"])
def delete_attendance(attendance_id):
    oid = valid_object_id(attendance_id)
    if oid is None:
        flash("Invalid attendance ID.", "error")
        return redirect(url_for("view_attendance"))

    result = attendance_collection.delete_one({"_id": oid})
    flash(
        "Attendance deleted successfully." if result.deleted_count else "Attendance record not found.",
        "success" if result.deleted_count else "error"
    )
    return redirect(url_for("view_attendance"))


# =========================================================
# LOW ATTENDANCE ALERTS
# =========================================================
@app.route("/alerts")
def alerts():
    alert_data = []
    for student in students_collection.find().sort("roll_no", ASCENDING):
        percentage = attendance_percentage(student["_id"])
        if percentage < 75:
            data = dict(student)
            data["percentage"] = percentage
            alert_data.append(data)

    return render_template("alerts.html", students=alert_data, limit=75)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False)
