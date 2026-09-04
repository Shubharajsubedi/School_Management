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
            


class Person(ABC):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @abstractmethod
    def get_roles(self):
        pass

    @abstractmethod    
    def register(self):
        pass

    @abstractmethod
    def show_details(self):
        pass
    

class Student(Person):
    def __init__(self, name, age, student_id):
        super().__init__(name, age)
        self.student_id = student_id
        self.grades = []

    def get_roles(self):
        return "Student"

    def register(self):
        data["students"].append({
            "name": self.name,
            "age": self.age,
            "student_id": self.student_id,
            "grades": self.grades
        })
        with open(databse, "w") as f:
            json.dump(data, f)

    def show_details(self):
        print(f"Name: {self.name}, Age: {self.age}, Student ID: {self.student_id}, Grades: {self.grades}")


print("press 1 to register a student")
print("press 2 to register a Teacher")
print("press 3 to add grades")
print("press 4 to show student details")
print("press 5 to show teacher details")

choice = int(input("Enter your choice: "))

if choice == 1:
    pass
elif choice == 2:
    pass
elif choice == 3:
    pass
elif choice == 4:
    pass
elif choice == 5:
    pass
else:
    pass
  
