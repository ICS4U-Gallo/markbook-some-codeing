"""
Markbook Application
Group members: 
"""
from typing import Dict


class Student:
    def __init__(self, first_name, last_name, gender, image, student_number, grade, email, comments):
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.image = image
        self.student_number = student_number
        self.grade = grade
        self.email = email
        self.comments = comments
        self.marks = {}

    def __str__(self):
        return "{0} {1} {2}".format(self.first_name, self.last_name, self.student_number)


    def get_student_num(self):
        return self.student_number

    def set_course(self, course_code):
        self.marks[course_code] = {}

    def create_assignment(self, course_code, assignment_name):
        if course_code not in self.marks:
            self.set_course(course_code)
        self.marks[course_code][assignment_name] = 0

    def set_assignment_mark(self, course_code, assignment_name, mark):
        self.marks[course_code][assignment_name] = mark

    def get_assignment_mark(self, course_code, assignment):
        return self.marks[course_code][assignment]

    def get_comment(self):
        return self.comments

    def set_comment(self, comments):
        self.comments = comments

    # calculate the average of a specific course, auto drop the lowest
    def get_assignment_average(self, course_code):
        if len(self.marks[course_code]) == 0:
            return 0
        sum_mark = 0
        for i in self.marks[course_code]:
            sum_mark += self.marks[course_code][i]

        values = []
        for value in self.marks[course_code].values():
            values.append(value)

        if len(self.marks[course_code]) == 1:
            return sum_mark
        return ((sum_mark - min(values)) / ((len(self.marks[course_code]) - 1)))


    # calculate the average of all courses
    def get_overall_average(self):
        if len(self.marks) == 0:
            return 0
        else:
            overall_sum = 0
            for course_code in self.marks:
                overall_sum += self.get_assignment_average(course_code)
            if len(self.marks) == 1:
                return overall_sum
            return overall_sum / len(self.marks)

    def get_course_marks(self, course_code):
        return self.marks[course_code]

    def assignment(self):
        return self.marks



class Assignment:
    def __init__(self, name, points, due):
        self.name = name
        self.points = points
        self.due = due
        self.course = None

    def __str__(self):
        return "{0}, worth {1} marks".format(self.name, str(self.points))

    def get_name(self):
        return self.name

    def get_worth(self):
        return self.points

    def set_course(self, course_code):
        self.course = course_code

    def get_course(self):
        return self.course


class Classroom:
    def __init__(self, course_code, course_name, period, teacher_name):
        self.course_code = course_code
        self.course_name = course_name
        self.period = period
        self.teacher_name = teacher_name
        self.student_list = []
        self.assignment_list = []

    def __repr__(self):
        return self.get_course_code()
    def get_course_code(self):
        """
        Return the course code
        :return:
        :rtype:
        """
        return self.course_code

    def get_info(self):
        """
        Print class information
        :return:
        :rtype:
        """
        return "{0}  \"{1}\"; period: {2}; Teacher: {3}".format(self.course_code,
                                                  self.course_name,
                                                  self.period,
                                                  self.teacher_name)

    def add_assignment(self, assignment):
        """
        Add an assignmnet to this classroom
        :param assignment:
        :type assignment:
        :return:
        :rtype:
        """
        assignment.set_course(self.course_code)
        self.assignment_list.append(assignment)
        for student in self.student_list:
            student.create_assignment(self.course_code, assignment.get_name())

    def remove_assignment(self, assignment):
        """
        Remove an assignment from this classroom if available.
        :param assignment:
        :type assignment:
        :return:
        :rtype:
        """
        if assignment in self.assignment_list:
            self.assignment_list.remove(assignment)

    def print_assignments(self):
        """
        Print all the assignments.
        :return:
        :rtype:
        """
        for assignment in self.assignment_list:
            print(assignment)

    def add_student(self, student):
        """
        Add a new student to this classroom
        :param student:
        :type student:
        :return:
        :rtype:
        """
        self.student_list.append(student)

    def remove_student(self, student):
        """
        Remove a student from this classroom if available.
        :param student:
        :type student:
        :return:
        :rtype:
        """
        if student in self.student_list:
            self.student_list.remove(student)

    def print_students(self):
        """
        Print all the students in this classroom
        :return:
        :rtype:
        """
        for student in self.student_list:
            print(student)

    def find_assignment_worth(self, a_n):
        """
        Helper function.
        Find the worth of an assignment naming a_n
        :param a_n:
        :return:
        :rtype:
        """
        for assignment in self.assignment_list:
            if assignment.get_name() == a_n:
                return assignment.get_worth()

    def get_assignment_scores(self, assignment_name):
        """
        Print all the scores of this class regarding to the assignment name
        :param assignment_name:
        :type assignment_name:
        :return:
        :rtype:
        """
        print("{0} {1}\n".format(self.course_code, assignment_name))
        for student in self.student_list:
            m = student.get_assignment_mark(self.course_code, assignment_name)
            print(student, "{0} / {1}".format(m, self.find_assignment_worth(assignment_name)))

    def get_assignment_average(self, assignment_name):
        """
        Get the average score of assignment_name
        :param assignment_name:
        :type assignment_name:
        :return:
        :rtype:
        """
        score_sum = 0
        score_tot = 0
        for student in self.student_list:
            m = student.get_assignment_mark(self.course_code, assignment_name)
            score_sum += m
            score_tot += 1
        print("{0} out of {1} average for {2}".format(score_sum / score_tot,
              self.find_assignment_worth(assignment_name), assignment_name))
        return score_sum/score_tot

    def set_mark(self, student_num, assignment_name, mark):
        student = None
        for i in self.student_list:
            if i.get_student_num() == student_num:
                student = i
        if student:
            student.set_assignment_mark(self.course_code, assignment_name, mark)

    def order_assignments(self, by):
        d = {}
        for assignment in self.assignment_list:
            a = assignment.get_name()
            s = self.get_assignment_average(a)
            d[a] = s
        print(self.get_course_code())
        if by == "alpha":
            for k in sorted(d.keys()):
                print(k, d[k])
        if by == "score":
            new_d = reverse_dict(d)
            for k in sorted(new_d.keys(), reverse=True):
                for v in sorted(new_d[k]):
                    print(v, k)

def reverse_dict(d):
    new_d = {}
    for key in d:
        if d[key] not in d:
            new_d[d[key]] = []
        new_d[d[key]].append(key)
    return new_d

if __name__ == "__main__":
    school = []
    print("Welcome to school management system v0.1!")
    print("Current Classes: \n", school)

    while True:
        operation = input("Please Enter a new command: [c]Create new class, [m]Manage a course, [r]Remove a course")
        if operation == "c":
            print("Creating new class. \nPlease enter: (if not decided, please enter TBD)")
            course_code = input("course code: ")
            course_name = input("course name: ")
            period = input("period: ")
            teacher_name = input("teacher name: ")
            new_class = Classroom(course_code, course_name, period, teacher_name)
            school.append(new_class)
            print("\nsuccessful!!\n")

        if operation == "m":
            print(school)
            code = input("Please select a course code: ")
            course = None
            for i in school:
                if i.get_course_code() == code:
                    course = i
            if course:
                print(course.get_info())
            else:
                print("Invalid course code!")

        if operation == "r":
            print("Remove a course. \n Please enter: (if not decided, p")



        print(school)



    # c = Classroom("ICS4U","Computer Science",2,"Mr. Gallo")
    # c.get_info()
    # s1 = Student("Charlie", "Guo", "male", "abc", 123, 12, "gamil", "hi")
    # s2 = Student("JAson", "He", "male", "abc", 100, 15, "mail", "hello")
    # c.add_student(s1)
    # c.add_student(s2)
    # c.print_students()
    #
    # print()
    # print()
    # a1 = Assignment("A1", 100, 10)
    # a2 = Assignment("A2", 100, 10)
    # a3 = Assignment("A3", 100, 10)
    # c.add_assignment(a2)
    # c.add_assignment(a1)
    # c.add_assignment(a3)
    # c.print_assignments()
    #
    # print()
    # print()
    # c.get_assignment_scores("A1")
    # c.get_assignment_average("A1")
    #
    #
    # c.set_mark(100, "A1", 90)
    # c.set_mark(123, "A1", 100)
    # c.set_mark(123, "A2", 95)
    # c.set_mark(100, "A3", 100)
    # c.set_mark(123, "A3", 100)
    #
    #
    # c.get_assignment_scores("A1")
    # c.get_assignment_average("A1")
    #
    # c.get_assignment_scores("A2")
    # c.get_assignment_average("A2")
    #
    # print(s1.get_assignment_average("ICS4U"))
    #
    # print()
    # print()
    # print(s1.get_overall_average())
    # print(s2.get_overall_average())
    # print(s1.get_course_marks("ICS4U"))
    #
    # print()
    # print()
    # c.order_assignments("alpha")
    # c.order_assignments("score")


# class Classroom:
#     def __init__(self):
#         self.course_code = None
#         self.course_name = None
#         self.period = None
#         self.teacher_name = None
#         self.student_list = []
#         self.assignments_list = []
#
#     def remove_student(self, student):
#         """Removes student from this classroom if the student is in it
#
#         Args:
#             student: The student to be removed
#             classroom: the class from which the student will be removed.
#         """
#         if student in self.student_list:
#             self.student_list.remove(student)
#
#     def add_student(self, student):
#         """add student to this classroom
#
#         Args:
#             student: The student to be added
#             classroom: the class from which the student will be added.
#         """
#         if student not in self.student_list and type(student).__name__ == "Student":
#             self.student_list.append(student)
#
#     def add_assignment(self, assignment):
#         if assignment not in self.assignments_list and type(assignment).__name__ == "Assignment":
#             self.assignments_list.append(assignment)
#
#     def remove_assignment(self, assignment):
#         """Removes assignment from this classroom if the assignment is in it
#
#         Args:
#             assignment: The assignment to be removed
#             classroom: the class from which the assignment will be removed.
#         """
#         if assignment in self.assignments_list:
#             self.assignments_list.remove(assignment)
#
#
#     def get_student_list(self):
#         return self.student_list
#
#     def get_assignment_list(self):
#         return self.assignments_list
#
#     def get_class_average(self):
#         sum_mark = 0
#         for student in self.student_list:
#             sum_mark += student.get_average_mark()
#         return sum_mark / len(self.student_list)
#
# class Assignment:
#     def __init__(self):
#         self.due = None
#         self.name = None
#         self.marks = None
#
#
#
#
# data = {
#     "student": [
#         {"students":""},
#         {"classroom":""},
#         {"kwargs":""},
#     ],
#     "class_room": [
#         {"course_code":""},
#         {"course_name":""},
#         {"period":""},
#         {"teacher":""},
#     ],
#     "assignments": [
#         {"name":""},
#         {"due":""},
#         {"points":""},
#     ],
# }
#
#
# def create_assignment(name: str, due: str, points: int) -> Dict:
#     """Creates an assignment represented as a dictionary
#
#     Args:
#         name: the name of the assignment.
#         due: the due date for the assignment.
#         points: what the assignment is out of (denominator).
#     Returns:
#         Assignment as a dictionary.
#     """
#     return {"name": name, "due": due, "points": points}
#
#
# def create_classroom(course_code: str, course_name: str, period: int, teacher: str) -> Dict:
#     """Creates a classroom dictionary"""
#
#     return {"course_code": course_code, \
#         "course_name": course_name, \
#         "period": period, \
#         "teacher": teacher, \
#         "student_list": [], \
#         "assignments_list": []}
#
#
# def calculate_average_mark(student: Dict) -> float:
#     """Calculates the average mark of a student"""
#     sum_mark = 0
#     for i in range(len(student["marks"])):
#         sum_mark += student["marks"][i]
#     return sum_mark / len(student["marks"])
#
#
# def add_student_to_classroom(student, classroom):
#     """Adds student to a classroom
#
#     Args:
#         student: Student dict
#         classroom: The classroom to add the student to
#     """
#     classroom["student_list"].append(student)
#
#
#
# def remove_student_from_classroom(student: Dict, classroom: Dict):
#     """Removes student from classroom
#
#     Args:
#         student: The student to be removed
#         classroom: the class from which the student will be removed.
#     """
#     classroom["student_list"].pop(classroom["student_list"].index(student))
#
#
#
#
# def edit_student(student: Dict, **kwargs: Dict):
#     """Edits the student's info with the provided key/value pairs
#
#     Args:
#         student: The student whose data needs to be udated.
#         **kwargs: KeyWordARGumentS. The key/value pairs of the
#             data that needs to be changed. Can come in the form
#             of a dictionary.
#     """
#     for key, value in kwargs.items():
#         if key in student:
#             student[key] = value
#
# if __name__ == "__main__":
#     print(create_assignment("123", "456", 789))
