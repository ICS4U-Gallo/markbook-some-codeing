"""
Markbook Application
Group members: 
"""
from typing import Dict


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