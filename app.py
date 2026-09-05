import json
from pathlib import Path
import streamlit as st
from abc import ABC, abstractmethod

# --- Data persistence ---
DATA_FILE = "school_data.json"

def load_data():
    """Load data from JSON file, return default structure if missing."""
    if Path(DATA_FILE).exists():
        with open(DATA_FILE, "r") as f:
            content = f.read()
            if content:
                return json.loads(content)
    return {"students": [], "teachers": []}

def save_data(data):
    """Save data to JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# --- Core classes (adapted for Streamlit) ---
class Persons(ABC):
    @staticmethod
    def validate_email(email):
        return "@" in email and "." in email

class Student(Persons):
    @staticmethod
    def register(data, name, age, student_id, email, roll_no):
        if not Persons.validate_email(email):
            return False, "Invalid email format."
        # Check duplicates
        for s in data["students"]:
            if s["student_id"] == student_id:
                return False, "Student ID already exists."
            if s["roll_no"] == roll_no:
                return False, "Roll number already exists."
        data["students"].append({
            "name": name,
            "age": age,
            "student_id": student_id,
            "email": email,
            "roll_no": roll_no,
            "grades": {}
        })
        save_data(data)
        return True, f"Student {name} with ID {student_id} registered successfully."

    @staticmethod
    def add_grade(data, student_id, subject, grade):
        for s in data["students"]:
            if s["student_id"] == student_id:
                s["grades"][subject] = grade
                save_data(data)
                return True, f"Grade {grade} added for {subject} (Student {student_id})."
        return False, "Student ID not found."

    @staticmethod
    def show_details(data, student_id):
        for s in data["students"]:
            if s["student_id"] == student_id:
                return s
        return None

class Teacher(Persons):
    @staticmethod
    def register(data, name, age, teacher_id, email, subject):
        if not Persons.validate_email(email):
            return False, "Invalid email format."
        for t in data["teachers"]:
            if t["teacher_id"] == teacher_id:
                return False, "Teacher ID already exists."
        data["teachers"].append({
            "name": name,
            "age": age,
            "teacher_id": teacher_id,
            "email": email,
            "subject": subject
        })
        save_data(data)
        return True, f"Teacher {name} with ID {teacher_id} registered successfully."

    @staticmethod
    def show_details(data, teacher_id):
        for t in data["teachers"]:
            if t["teacher_id"] == teacher_id:
                return t
        return None

# --- Streamlit UI ---
def main():
    st.set_page_config(page_title="School Management System", layout="wide")
    st.title("🏫 School Management System")

    # Load data once and keep in session state
    if "data" not in st.session_state:
        st.session_state.data = load_data()

    data = st.session_state.data

    # Sidebar navigation
    menu = st.sidebar.radio(
        "Navigation",
        ["Register Student", "Register Teacher", "Add Grades",
         "View Student Details", "View Teacher Details",
         "All Students", "All Teachers"]
    )

    # ----------------- Register Student -----------------
    if menu == "Register Student":
        st.header("Register New Student")
        with st.form("register_student_form"):
            name = st.text_input("Full Name")
            age = st.number_input("Age", min_value=1, step=1)
            student_id = st.text_input("Student ID")
            email = st.text_input("Email")
            roll_no = st.text_input("Roll Number")
            submitted = st.form_submit_button("Register")
            if submitted:
                if not all([name, student_id, email, roll_no]):
                    st.error("Please fill in all fields.")
                else:
                    success, message = Student.register(data, name, age, student_id, email, roll_no)
                    if success:
                        st.success(message)
                        st.session_state.data = data  # update session state
                    else:
                        st.error(message)

    # ----------------- Register Teacher -----------------
    elif menu == "Register Teacher":
        st.header("Register New Teacher")
        with st.form("register_teacher_form"):
            name = st.text_input("Full Name")
            age = st.number_input("Age", min_value=1, step=1)
            teacher_id = st.text_input("Teacher ID")
            email = st.text_input("Email")
            subject = st.text_input("Subject Taught")
            submitted = st.form_submit_button("Register")
            if submitted:
                if not all([name, teacher_id, email, subject]):
                    st.error("Please fill in all fields.")
                else:
                    success, message = Teacher.register(data, name, age, teacher_id, email, subject)
                    if success:
                        st.success(message)
                        st.session_state.data = data
                    else:
                        st.error(message)

    # ----------------- Add Grades -----------------
    elif menu == "Add Grades":
        st.header("Add Student Grade")
        # get list of student IDs for dropdown
        student_ids = [s["student_id"] for s in data["students"]]
        if not student_ids:
            st.warning("No students registered yet.")
        else:
            with st.form("add_grade_form"):
                student_id = st.selectbox("Select Student ID", student_ids)
                subject = st.text_input("Subject")
                grade = st.text_input("Grade (e.g., A, B+)")
                submitted = st.form_submit_button("Add Grade")
                if submitted:
                    if not subject or not grade:
                        st.error("Please enter subject and grade.")
                    else:
                        success, message = Student.add_grade(data, student_id, subject, grade)
                        if success:
                            st.success(message)
                            st.session_state.data = data
                        else:
                            st.error(message)

    # ----------------- View Student Details -----------------
    elif menu == "View Student Details":
        st.header("Student Details")
        student_ids = [s["student_id"] for s in data["students"]]
        if not student_ids:
            st.info("No students available.")
        else:
            selected_id = st.selectbox("Select Student ID", student_ids)
            student = Student.show_details(data, selected_id)
            if student:
                st.json(student)  # simple display; can format better
                # nicer display
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Name", student["name"])
                    st.metric("Age", student["age"])
                    st.metric("Student ID", student["student_id"])
                with col2:
                    st.metric("Email", student["email"])
                    st.metric("Roll Number", student["roll_no"])
                    st.metric("Grades", student["grades"] if student["grades"] else "None")
            else:
                st.error("Student not found.")

    # ----------------- View Teacher Details -----------------
    elif menu == "View Teacher Details":
        st.header("Teacher Details")
        teacher_ids = [t["teacher_id"] for t in data["teachers"]]
        if not teacher_ids:
            st.info("No teachers available.")
        else:
            selected_id = st.selectbox("Select Teacher ID", teacher_ids)
            teacher = Teacher.show_details(data, selected_id)
            if teacher:
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Name", teacher["name"])
                    st.metric("Age", teacher["age"])
                    st.metric("Teacher ID", teacher["teacher_id"])
                with col2:
                    st.metric("Email", teacher["email"])
                    st.metric("Subject", teacher["subject"])
            else:
                st.error("Teacher not found.")

    # ----------------- All Students -----------------
    elif menu == "All Students":
        st.header("All Students")
        if data["students"]:
            # Convert grades dict to string for display
            students_display = []
            for s in data["students"]:
                s_copy = s.copy()
                s_copy["grades"] = str(s_copy["grades"])
                students_display.append(s_copy)
            st.dataframe(students_display, use_container_width=True)
        else:
            st.info("No students registered yet.")

    # ----------------- All Teachers -----------------
    elif menu == "All Teachers":
        st.header("All Teachers")
        if data["teachers"]:
            st.dataframe(data["teachers"], use_container_width=True)
        else:
            st.info("No teachers registered yet.")

if __name__ == "__main__":
    main()