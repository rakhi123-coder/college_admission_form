from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

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

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = {
            "full_name": request.form.get("full_name"),
            "gender": request.form.get("gender"),
            "email": request.form.get("email"),
            "phone": request.form.get("phone"),
            "address": request.form.get("address"),
            "course": request.form.get("course"),
            "admission_year": request.form.get("admission_year"),
            "guardian_name": request.form.get("guardian_name"),
            "guardian_contact": request.form.get("guardian_contact")
        }
        students_collection.insert_one(data)
        # ✅ Use url_for for a proper redirect with query string
        return redirect(url_for("register", success="true"))

    # ✅ Check the query param properly
    success = request.args.get("success") == "true"
    return render_template("register.html", courses=AVAILABLE_COURSES, success=success)

@app.route("/students")
def view_students():
    students = list(students_collection.find())
    return render_template("students.html", students=students)

if __name__ == "__main__":
    app.run(debug=True)
