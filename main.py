import json 
from abc import ABC, abstractmethod

from pathlib import Path

databse = "school_data.json"
data = {
    "students": [],
    "teachers": []
}

if Path(databse).exists():
    with open(databse, "r") as f:
        content = f.read()
        if content:
            data = json.loads(content)
            

def save():
    with open(databse, "w") as f:
        json.dump(data, f, indent=4)

class Persons(ABC):

    @abstractmethod
    def get_roles(self):
        pass

    @abstractmethod    
    def register(self):
        pass

    @abstractmethod
    def show_details(self):
        pass

    @staticmethod
    def validate_email(email):
        if "@" in email and "." in email:
            return True
        else:
            return False


class Student(Persons):

    def get_roles(self):
        return "Student"

    def register(self):
        name = input("Enter student name: ")
        age = int(input("Enter student age: "))
        student_id = input("Enter student ID: ")
        email = input("Enter student email: ")
        roll_no = input ("Enter student roll number: ")
        
        
        if not Persons.validate_email(email):
            print("Invalid email format.")
            return

        for i in data["students"]:
            if i["student_id"] == student_id:
                print("Student ID already exists.")
                return

            if i["roll_no"] == roll_no:
                print("Roll number already exists.")
                return

        data["students"].append({
            "name": name,
            "age": age,
            "student_id": student_id,
            "email": email,
            "roll_no": roll_no, 
            "grades": {}
        })   

        save()

        print(f"Student :{name} with ID : {student_id} registered successfully.")    

    def add_grades(self):
        student_id = input("Enter student ID: ")
        subject = input("Enter subject: ")
        grade = input("Enter grade: ")

        for i in data["students"]:
            if i["student_id"] == student_id:
                i["grades"][subject] = grade
                save()
                print(f"Grade {grade} added for subject {subject} for student ID {student_id}.")
                return

        print("Student ID not found.")    

    def show_details(self):
        name = input("Enter student name: ")
        roll_no = input("Enter student roll number: ")
        for i in data["students"]:
            if i["roll_no"] == roll_no and i["name"] == name:
                print(f"Name: {i['name']} \nAge: {i['age']} \nStudent ID: {i['student_id']} \nEmail: {i['email']} \nRoll Number: {i['roll_no']} \nGrades: {i['grades']}")
                return
class Teacher(Persons):

    def get_roles(self):
        return "Teacher"

    def register(self):
        name = input("Enter teacher name: ")
        age = int(input("Enter teacher age: "))
        teacher_id = input("Enter teacher ID: ")
        email = input("Enter teacher email: ")
        subject = input("Enter subject taught by the teacher: ")

        if not Persons.validate_email(email):
            print("Invalid email format.")
            return

        for i in data["teachers"]:
            if i["teacher_id"] == teacher_id:
                print("Teacher ID already exists.")
                return

        data["teachers"].append({
            "name": name,
            "age": age,
            "teacher_id": teacher_id,
            "email": email,
            "subject": subject
        })

        save()

        print(f"Teacher :{name} with ID : {teacher_id} registered successfully.")

    def show_details(self):
            name = input("Enter teacher name: ")
            roll_no = input("Enter teacher ID: ")
            for i in data["teachers"]:
                if i["teacher_id"] == roll_no and i["name"] == name:
                    print(f"Name: {i['name']} \nAge: {i['age']} \nTeacher ID: {i['teacher_id']} \nEmail: {i['email']} \nSubject: {i['subject']}")
                    return
            
        



      
std = Student()
tec = Teacher()

print("press 1 to register a student")
print("press 2 to register a Teacher")
print("press 3 to add grades")
print("press 4 to show student details")
print("press 5 to show teacher details")

choice = int(input("Enter your choice: "))

if choice == 1:
    std.register()
elif choice == 2:
    tec.register()
elif choice == 3:
    std.add_grades()
elif choice == 4:
    std.show_details()
elif choice == 5:
    tec.show_details()
else:
    pass
  
