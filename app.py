from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# MongoDB setup
client = MongoClient("mongodb+srv://iamrakhi055:CaztWcrqF6qihKYg@collegeadmission.bukxpit.mongodb.net/?retryWrites=true&w=majority&appName=CollegeAdmission")
db = client["college_db"]
students_collection = db["students"]

# Hardcoded courses list
AVAILABLE_COURSES = [
    "BCA", "BBA", "MCA", "BA", "B.Tech", "M.Tech",
    "MBA", "B.Com", "M.Com", "B.Sc", "M.Sc", "B.Ed",
    "B.Arch", "M.Arch", "BPharma"
]

from bson.objectid import ObjectId

@app.route("/student/<student_id>")
def view_student(student_id):
    student = students_collection.find_one({"_id": ObjectId(student_id)})
    return render_template("student_profile.html", student=student)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        def save_file(field_name):
            file = request.files.get(field_name)
            if file and file.filename:
                filename = secure_filename(file.filename)
                path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(path)
                return filename
            return None
        student = {
            "first_name": request.form.get("first_name"),
            "middle_name": request.form.get("middle_name", ""),
            "last_name": request.form.get("last_name"),
            "dob": request.form.get("dob"),

            "father_name": request.form.get("father_name"),
            "father_occupation": request.form.get("father_occupation"),
            "father_income": request.form.get("father_income"),

            "mother_name": request.form.get("mother_name"),
            "mother_occupation": request.form.get("mother_occupation"),
            "mother_income": request.form.get("mother_income"),

            "email": request.form.get("email"),
            "phone": request.form.get("phone"),

            "permanent_address": request.form.get("permanent_address"),
            "pin_code": request.form.get("pin_code"),
            "correspondence_address": request.form.get("correspondence_address"),

            "caste": request.form.get("caste"),
            "religion": request.form.get("religion"),

            "marks_10th": request.form.get("marks_10th"),
            "marks_12th": request.form.get("marks_12th"),

            # Save filenames only
            "caste_certificate_filename": save_file("caste_certificate"),
            "residential_certificate_filename": save_file("residential_certificate"),
            "photo_filename": save_file("photo")
        }
        students_collection.insert_one(student)
        return redirect(url_for("register", success="true"))

    success = request.args.get("success") == "true"
    return render_template("register.html", courses=AVAILABLE_COURSES, success=success)

@app.route("/students")
def view_students():
    students = list(students_collection.find())
    return render_template("students.html", students=students)

if __name__ == "__main__":
    app.run(debug=True)
