"""
Markbook Application
Group members: 
"""
from typing import Dict

class Student:
    def __init__(self):
        self.first_name = None
        self.last_name = None
        self.gender = None
        self.image = None
        self.student_number = None
        self.grade = None
        self.email = None
        self.marks = []
        self.comments = None

    def get_average_mark(self):
        if len(self.marks) == 0:
            return 0
        elif len(self.marks) > 1:
            sum_mark = 0
            for i in range(len(self.marks)):
                sum_mark += self.marks[i]
            return (sum_mark - min(self.marks)) / (len(self.marks)-1)
        return self.marks[0]

    def add_mark(self, new_mark):
        self.marks.append(new_mark)

class Classroom:
    def __init__(self):
        self.course_code = None
        self.course_name = None
        self.period = None
        self.teacher_name = None
        self.student_list = []
        self.assignments_list = []

    def remove_student(self, student):
        """Removes student from this classroom if the student is in it

        Args:
            student: The student to be removed
            classroom: the class from which the student will be removed.
        """
        if student in self.student_list:
            self.student_list.remove(student)

    def add_student(self, student):
        """add student to this classroom

        Args:
            student: The student to be added
            classroom: the class from which the student will be added.
        """
        if student not in self.student_list and type(student).__name__ == "Student":
            self.student_list.append(student)

    def add_assignment(self, assignment):
        if assignment not in self.assignments_list and type(assignment).__name__ == "Assignment":
            self.assignments_list.append(assignment)

    def remove_assignment(self, assignment):
        """Removes assignment from this classroom if the assignment is in it

        Args:
            assignment: The assignment to be removed
            classroom: the class from which the assignment will be removed.
        """
        if assignment in self.assignments_list:
            self.assignments_list.remove(assignment)


    def get_student_list(self):
        return self.student_list

    def get_assignment_list(self):
        return self.assignments_list

    def get_class_average(self):
        sum_mark = 0
        for student in self.student_list:
            sum_mark += student.get_average_mark()
        return sum_mark / len(self.student_list)

class Assignment:
    def __init__(self):
        self.due = None
        self.name = None
        self.marks = None












data = {
    "student": [
        {"students":""},
        {"classroom":""},
        {"kwargs":""},
    ],
    "class_room": [
        {"course_code":""},
        {"course_name":""},
        {"period":""},
        {"teacher":""},
    ],
    "assignments": [
        {"name":""},
        {"due":""},
        {"points":""},
    ],    
}


def create_assignment(name: str, due: str, points: int) -> Dict:
    """Creates an assignment represented as a dictionary
    
    Args:
        name: the name of the assignment.
        due: the due date for the assignment.
        points: what the assignment is out of (denominator).
    Returns:
        Assignment as a dictionary.
    """
    return {"name": name, "due": due, "points": points}


def create_classroom(course_code: str, course_name: str, period: int, teacher: str) -> Dict:
    """Creates a classroom dictionary"""

    return {"course_code": course_code, \
        "course_name": course_name, \
        "period": period, \
        "teacher": teacher, \
        "student_list": [], \
        "assignments_list": []}


def calculate_average_mark(student: Dict) -> float:
    """Calculates the average mark of a student"""
    sum_mark = 0
    for i in range(len(student["marks"])):
        sum_mark += student["marks"][i]
    return sum_mark / len(student["marks"])


def add_student_to_classroom(student, classroom):
    """Adds student to a classroom

    Args:
        student: Student dict
        classroom: The classroom to add the student to
    """
    classroom["student_list"].append(student)



def remove_student_from_classroom(student: Dict, classroom: Dict):
    """Removes student from classroom

    Args:
        student: The student to be removed
        classroom: the class from which the student will be removed.
    """
    classroom["student_list"].pop(classroom["student_list"].index(student))




def edit_student(student: Dict, **kwargs: Dict):
    """Edits the student's info with the provided key/value pairs

    Args:
        student: The student whose data needs to be udated.
        **kwargs: KeyWordARGumentS. The key/value pairs of the
            data that needs to be changed. Can come in the form
            of a dictionary.
    """
    for key, value in kwargs.items():
        if key in student:
            student[key] = value
    
if __name__ == "__main__":
    print(create_assignment("123", "456", 789))
