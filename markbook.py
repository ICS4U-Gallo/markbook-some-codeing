"""
Markbook Application
Group members: Yingchen Ma, Charlie Guo, Simon Li
"""
from typing import Dict
from tkinter import *


class Student:
    def __init__(self, first_name, last_name, gender, image, student_number,
                 grade, email, comments):
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
        return "{0} {1} {2}".format(self.first_name, self.last_name,
                                    self.student_number)

    def get_info(self):
        return self.__str__()

    def get_student_num(self):
        return self.student_number

    def get_name(self):
        return self.first_name

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
        return ((sum_mark - min(values)) /
                ((len(self.marks[course_code]) - 1)))

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
        return "{0} {1}; period: {2}; Teacher: {3}".format(
            self.course_code, self.course_name, self.period, self.teacher_name)

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

    def remove_assignment(self, assignment_name):
        """
        Remove an assignment from this classroom if available.
        :param assignment:
        :type assignment:
        :return:
        :rtype:
        """
        for a in self.assignment_list:
            if a.get_name() == assignment_name:
                self.assignment_list.remove(a)

    def print_assignments(self):
        """
        Print all the assignments.
        :return:
        :rtype:
        """
        s = ""
        for assignment in self.assignment_list:
            s += str(assignment) + "\n"

        return s

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
            print(student, "{0} / {1}".format(
                m, self.find_assignment_worth(assignment_name)))

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
        print("{0} out of {1} average for {2}".format(
            score_sum / score_tot, self.find_assignment_worth(assignment_name),
            assignment_name))
        return score_sum / score_tot

    def set_mark(self, student_num, assignment_name, mark):
        student = None
        for i in self.student_list:
            if i.get_student_num() == student_num:
                student = i
        if student:
            student.set_assignment_mark(
                self.course_code, assignment_name, mark)

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
        if d[key] not in new_d:
            new_d[d[key]] = []
        new_d[d[key]].append(key)
    return new_d


# Graphic User Interface
# First page
def xuanxiang1pg():
    global root0
    root0 = Tk()
    root0.title("School")
    root0.geometry("240x320")
    root0.resizable(width=True, height=True)
    # prompt
    L_title = Label(root0, text='Please select')
    L_title.config(font='Helvetica -15 bold', fg='black')
    L_title.place(x=10, y=10, )
    # classroom
    B_250 = Button(root0, text="Classroom", command=lambda: [ketangx1pg()])
    B_250.place(x=40, y=100)
    # student
    B_251 = Button(root0, text="Student", command=ketangx2pg)
    B_251.place(x=40, y=150)
    root0.mainloop()


# class option
def ketangx1pg():
    global root1
    root1 = Tk()

    root1.title("Class Option")
    root1.geometry("240x320")
    root1.resizable(width=True, height=True)

    # label
    L_title = Label(root1, text='Please select')
    L_title.config(font='Helvetica -15 bold', fg='blue')
    L_title.place(x=60, y=10, anchor="center")
    # create course
    B_11 = Button(root1, text="Create course", command=chuangjian1pg)
    B_11.place(x=40, y=60)
    # manage course
    B_12 = Button(root1, text="Manage course", command=guanli1pg)
    B_12.place(x=40, y=120)
    root1.mainloop()


# create classroom
def chuangjian1pg():
    global course_code_entry, course_name_entry, teacher_name_entry, period_entry
    root10 = Tk()

    root10.title("Creat Classroom")
    root10.geometry("480x640")
    root10.resizable(width=True, height=True)

    # Create Class
    L_title = Label(root10, text='Creat a course')
    L_title.config(font='Helvetica -15 bold', fg='blue')
    L_title.place(x=50, y=10, anchor="center")
    # Course Code
    L_title = Label(root10, text='Course code')
    L_title.config(font='Helvetica -15 bold', fg='red')
    L_title.place(x=70, y=50, anchor="center")
    # Input
    course_code_entry = Entry(root10)
    course_code_entry.pack(padx=100, pady=30)
    # Course Name
    L_title = Label(root10, text='Course name')
    L_title.config(font='Helvetica -15 bold', fg='red')
    L_title.place(x=50, y=100, anchor="center")
    # Input
    course_name_entry = Entry(root10)
    course_name_entry.pack(padx=100, pady=5)
    # teacher name
    L_title = Label(root10, text='Teacher name')
    L_title.config(font='Helvetica -15 bold', fg='red')
    L_title.place(x=50, y=150, anchor="center")
    # Input
    teacher_name_entry = Entry(root10)
    teacher_name_entry.pack(padx=100, pady=30)
    # 科目位置
    L_title = Label(root10, text='Period')
    L_title.config(font='Helvetica -15 bold', fg='red')
    L_title.place(x=50, y=200, anchor="center")
    # 输入按钮
    period_entry = Entry(root10)
    # 输入框赋值在period变量
    period_entry.pack(padx=100, pady=3)
    # 继续返回按钮
    B_15 = Button(root10, text="next", command=abc)
    B_15.place(x=300, y=450)
    root10.mainloop()


def abc():
    global school_classes
    course_code = course_code_entry.get()
    course_name = course_name_entry.get()
    teacher_name = teacher_name_entry.get()
    period = period_entry.get()
    new_class = Classroom(course_code, course_name, period, teacher_name)
    school_classes.append(new_class)
    print(school_classes)
    chuangjian1cgpg()


# class mani
def guanli1pg():
    global root11, school_classes, class_inf
    root11 = Tk()

    root11.title("class mani")
    root11.geometry("640x480")
    root11.resizable(width=True, height=True)

    print(school_classes)
    i = 0
    for c in school_classes:
        c_button = Button(root11, text=c.get_course_code(), command=lambda: [inclass(c)])
        c_button.place(x=130 + 100 * i, y=100)
        i += 1


def inclass(c):
    root = Tk()
    root.title("Management")
    root.geometry("640x480")
    # title
    L_title = Label(root, text='Manage')
    L_title.config(font='Helvetica -15 bold', fg='blue')
    L_title.place(x=150, y=20, anchor="center")
    # assignment option
    B_30 = Button(root, text="Assignment", command=lambda: [ketangzypg(c)])
    B_30.place(x=130, y=200)
    # student option
    B_31 = Button(root, text="Student", command=lambda: [ketangxspg(c)])
    B_31.place(x=130, y=300)


def chuangjian1cgpg():
    """
    prompt function （Success)
    :return: prompt
    """
    global root20
    root20 = Tk()

    root20.title("You are all set")
    root20.geometry("240x320")
    root20.resizable(width=True, height=True)

    # 标签
    L_title = Label(root20, text='Success')
    L_title.config(font='Helvetica -20 bold', fg='blue')
    L_title.place(x=50, y=100, anchor="center")


def bcd(clas, a, b, c):
    new_assignment = Assignment(a, b, c)
    clas.add_assignment(new_assignment)
    chuangjian1cgpg()


# Add assignment
def ketangzytjpg(c):
    global root31, name_entry, points_entry, due_entry
    root31 = Tk()

    root31.title("Add Assignment")
    root31.geometry("480x640")
    root31.resizable(width=True, height=True)
    # 作业添加
    L_title = Label(root31, text='Creat Assignment')
    L_title.config(font='Helvetica -15 bold', fg='blue')
    L_title.place(x=150, y=20, anchor="center")
    # 作业名
    L_title = Label(root31, text='Name')
    L_title.config(font='Helvetica -15 bold', fg='red')
    L_title.place(x=100, y=100, anchor="center")
    # 输入按钮
    name_entry = Entry(root31)
    # 输入框赋值在name变量
    name_entry.pack(padx=150, pady=90)
    # 作业比重
    L_title = Label(root31, text='Worth')
    L_title.config(font='Helvetica -15 bold', fg='red')
    L_title.place(x=100, y=210, anchor="center")
    # 输入按钮
    points_entry = Entry(root31)
    # 输入框赋值在points变量
    points_entry.pack(padx=150, pady=0)
    # 课程号
    L_title = Label(root31, text='Due Date')
    L_title.config(font='Helvetica -15 bold', fg='red')
    L_title.place(x=100, y=280, anchor="center")
    # 输入按钮
    due_entry = Entry(root31)
    # 输入框赋值在due变量
    due_entry.pack(padx=150, pady=50)

    B_18 = Button(root31, text="next", command=lambda: [bcd(c, name_entry.get(), points_entry.get(), due_entry.get())])
    B_18.place(x=300, y=500)
    root31.mainloop()


# Assignment
def ketangzypg(c):
    global root21
    root21 = Tk()

    root21.title("Class Assignment")
    root21.geometry("640x480")
    root21.resizable(width=True, height=True)
    # 管理作业
    L_title = Label(root21, text='manage assignment')
    L_title.config(font='Helvetica -15 bold', fg='blue')
    L_title.place(x=150, y=20, anchor="center")
    # 课堂作业添加
    B_30 = Button(root21, text="add assignment", command=lambda: [ketangzytjpg(c)])
    B_30.place(x=130, y=100)
    # 课堂作业移除
    B_31 = Button(root21, text="remove assignment", command=lambda: [ketangzyscpg(c)])
    B_31.place(x=130, y=200)
    # 课堂作业分数管理
    B_31 = Button(root21, text="manage mark", command=lambda: [ketangzyfsglpg(c)])
    B_31.place(x=130, y=300)
    # 课堂作业信息
    B_32 = Button(root21, text="assignment info", command=lambda: [ketangzyxxpg(c)])
    B_32.place(x=130, y=400)


# Delete Assignment
def ketangzyscpg(c):
    global root44
    root44 = Tk()

    root44.title("delete homework")
    root44.geometry("640x480")
    root44.resizable(width=True, height=True)
    # 课堂作业删除
    L_title = Label(root44, text='remove assignment')
    L_title.config(font='Helvetica -15 bold', fg='blue')
    L_title.place(x=150, y=50, anchor="center")
    # 输入按钮
    name = Entry(root44)
    # 输入框赋值在e变量
    name.pack(padx=100, pady=40)
    # 继续
    B_21 = Button(root44, text="next", command=lambda: [cde(c, name.get())])
    B_21.place(x=300, y=400)
    root44.mainloop()


def cde(c, name):
    c.remove_assignment(name)
    chuangjian1cgpg()


# Assignment Info
def ketangzyxxpg(c):
    global root32
    root32 = Tk()

    root32.title("homework info")
    root32.geometry("640x480")
    root32.resizable(width=True, height=True)
    l = Label(root32, text=c.print_assignments())
    l.place(x=100, y=100, anchor="center")


# Add marks to assignment
def ketangzyfstjpg(c):
    global root71
    root71 = Tk()
    root71.title("Add Mark")
    root71.geometry("480x640")
    root71.resizable(width=True, height=True)
    # 作业分数添加
    L_title = Label(root71, text='add assignment mark')
    L_title.config(font='Helvetica -15 bold', fg='blue')
    L_title.place(x=150, y=20, anchor="center")
    # 课程号
    L_title = Label(root71, text='course code')
    L_title.config(font='Helvetica -15 bold', fg='red')
    L_title.place(x=100, y=100, anchor="center")
    # 输入按钮
    course = Entry(root71)
    # 输入框赋值在course变量
    course.pack(padx=150, pady=90)
    # 学生号
    L_title = Label(root71, text='student number')
    L_title.config(font='Helvetica -15 bold', fg='red')
    L_title.place(x=100, y=210, anchor="center")
    # 输入按钮
    g3 = Entry(root71)
    # 输入框赋值在e变量
    g3.pack(padx=150, pady=0)
    # 作业
    L_title = Label(root71, text='assignment')
    L_title.config(font='Helvetica -15 bold', fg='red')
    L_title.place(x=100, y=280, anchor="center")
    # 输入按钮
    g4 = Entry(root71)
    # 输入框赋值在e变量
    g4.pack(padx=150, pady=50)
    # 分数
    L_title = Label(root71, text='mark')
    L_title.config(font='Helvetica -15 bold', fg='red')
    L_title.place(x=100, y=350, anchor="center")
    # 输入按钮
    g5 = Entry(root71)
    # 输入框赋值在e变量
    g5.pack(padx=150, pady=1)
    # 继续（添加移除）按钮

    B_37 = Button(root71, text="add", command=lambda: [efg(c, g3.get(), g4.get(), g5.get())])
    B_37.place(x=150, y=500)
    root71.mainloop()


def efg(clas, a, b, c):
    clas.set_mark(a, b, c)
    chuangjian1cgpg()


###
def ketangzyfsscpg():
    global root72
    root72 = Tk()
    root72.title("remove mark")
    root72.geometry("480x640")
    root72.resizable(width=True, height=True)
    # 作业分数添加
    L_title = Label(root72, text='remove assignment mark')
    L_title.config(font='Helvetica -15 bold', fg='blue')
    L_title.place(x=150, y=20, anchor="center")
    # 课程号
    L_title = Label(root72, text='course code')
    L_title.config(font='Helvetica -15 bold', fg='red')
    L_title.place(x=100, y=100, anchor="center")
    # 输入按钮
    g2 = Entry(root72)
    # 输入框赋值在e变量
    g2.pack(padx=150, pady=90)
    # 学生号
    L_title = Label(root72, text='student number')
    L_title.config(font='Helvetica -15 bold', fg='red')
    L_title.place(x=100, y=210, anchor="center")
    # 输入按钮
    g3 = Entry(root72)
    # 输入框赋值在e变量
    g3.pack(padx=150, pady=0)
    # 作业
    L_title = Label(root72, text='assignment')
    L_title.config(font='Helvetica -15 bold', fg='red')
    L_title.place(x=100, y=280, anchor="center")
    # 输入按钮
    g4 = Entry(root72)
    # 输入框赋值在e变量
    g4.pack(padx=150, pady=50)
    # 分数
    L_title = Label(root72, text='mark')
    L_title.config(font='Helvetica -15 bold', fg='red')
    L_title.place(x=100, y=350, anchor="center")
    # 输入按钮
    g5 = Entry(root72)
    # 输入框赋值在e变量
    g5.pack(padx=150, pady=1)
    # 继续（添加移除）按钮
    B_37 = Button(root72, text="remove", command=chuangjian1cgpg)
    B_37.place(x=200, y=500)
    root72.mainloop()


# 7课堂学生分数信息
def ketangxsfsxxpg():
    root36 = Tk()

    root36.title("student mark info")
    root36.geometry("640x480")
    root36.resizable(width=True, height=True)
    # 管理学生分数
    L_title = Label(root36, text='mark info')
    L_title.config(font='Helvetica -15 bold', fg='blue')
    L_title.place(x=150, y=20, anchor="center")


# 6Manage Assignment marks
def ketangzyfsglpg(c):
    global root61
    root61 = Tk()

    root61.title("Manage Assignment Mark")
    root61.geometry("640x480")
    root61.resizable(width=True, height=True)
    # 管理作业
    L_title = Label(root61, text='manage assignment mark')
    L_title.config(font='Helvetica -15 bold', fg='blue')
    L_title.place(x=150, y=20, anchor="center")
    # 课堂作业添加
    B_30 = Button(
        root61, text="add assignment mark", command=lambda: [ketangzyfstjpg(c)])
    B_30.place(x=130, y=100)
    # 课堂作业移除
    B_31 = Button(
        root61, text="remove assignment mark", command=ketangzyfsscpg)
    B_31.place(x=130, y=200)
    # 课堂作业显示
    B_31 = Button(root61, text="info", command=ketangxsfsxxpg)
    B_31.place(x=130, y=300)


# Add student to classroom
def ketangxstjpg(c):
    global root35
    root35 = Tk()
    root35.title("add student to class")
    root35.geometry("480x640")
    root35.resizable(width=True, height=True)
    # Add student
    L_title = Label(root35, text='add student')
    L_title.config(font='Helvetica -15 bold', fg='blue')
    L_title.place(x=80, y=100, anchor="center")
    # Input wanted student
    namea = Entry(root35)
    namea.pack(padx=100, pady=90)
    # Delete specific student
    L_title = Label(root35, text='remove student')
    L_title.config(font='Helvetica -15 bold', fg='blue')
    L_title.place(x=80, y=200, anchor="center")
    namej = Entry(root35)
    namej.pack(padx=100, pady=0)

    B_21 = Button(root35, text="next", command=lambda: [hij(c, namea.get(), namej.get())])
    B_21.place(x=300, y=450)
    root35.mainloop()


def hij(c, namea, namej):
    new = None
    rem = None
    for student in school_students:
        if student.get_name() == namea:
            new = student
        if student.get_name() == namej:
            rem = student

    if new:
        c.add_student(new)
    if rem:
        c.remove_student(rem)
    chuangjian1cgpg()


# 5课堂学生
def ketangxspg(c):
    global root22
    root22 = Tk()

    root22.title("Student in class")
    root22.geometry("640x480")
    root22.resizable(width=True, height=True)
    # 管理学生
    L_title = Label(root22, text='manage student')
    L_title.config(font='Helvetica -15 bold', fg='blue')
    L_title.place(x=150, y=20, anchor="center")
    # 课堂学生添加,移除
    B_40 = Button(
        root22, text="add or remove student", command=lambda: [ketangxstjpg(c)])
    B_40.place(x=130, y=100)
    # 课堂学生显示
    B_42 = Button(root22, text="student list", command=lambda: [ketangxsxspg(c)])
    B_42.place(x=130, y=300)


# 4课程信息
def xinxi1pg():
    global root12
    root12 = Tk()

    root12.title("Class Info")
    root12.geometry("1280x720")
    root12.resizable(width=True, height=True)
    # 信息
    L_title = Label(root12, text='info')
    L_title.config(font='Helvetica -20 bold', fg='blue')
    L_title.place(x=50, y=50, anchor="center")
    # 课程名
    L_title = Label(root12, text='course name:')
    L_title.config(font='Helvetica -15 bold', fg='blue')
    L_title.place(x=100, y=200, anchor="center")
    # 科目位置
    L_title = Label(root12, text='period:')
    L_title.config(font='Helvetica -15 bold', fg='blue')
    L_title.place(x=100, y=400, anchor="center")
    # 老师名
    L_title = Label(root12, text='teacher name:')
    L_title.config(font='Helvetica -15 bold', fg='blue')
    L_title.place(x=100, y=600, anchor="center")
    root12.mainloop()


# 5学生作业信息
def xszyxxpg():
    global root2
    root76 = Tk()

    root76.title("Assignment Info")
    root76.geometry("640x480")
    root76.resizable(width=True, height=True)
    # 标签
    L_title = Label(root76, text='Assignment Info')
    L_title.config(font='Helvetica -15 bold', fg='blue')
    L_title.place(x=60, y=10, anchor="center")


# 5学生评论
def xsplpg():
    root77 = Tk()

    root77.title("Comment")
    root77.geometry("640x480")
    root77.resizable(width=True, height=True)
    # 标签

    L_title = Label(root77, text='Comment')
    L_title.config(font='Helvetica -15 bold', fg='blue')
    L_title.place(x=60, y=10, anchor="center")


# 4学生管理
def ketangx3pg():
    global root2, root11, school_students
    root39 = Tk()

    root39.title("student manage")
    root39.geometry("640x480")
    root39.resizable(width=True, height=True)

    i = 0
    for s in school_students:
        s_button = Button(root39, text=s.get_name(), command=lambda: [inStu(s)])
        s_button.place(x=130 + 100 * i, y=100)
        i += 1
    root39.mainloop()


def inStu(s):
    root = Tk()
    root.title("Student Info")
    root.geometry("640x480")
    # 课堂管理
    L_title = Label(root, text='Info')
    L_title.config(font='Helvetica -15 bold', fg='blue')
    L_title.place(x=150, y=20, anchor="center")
    l = Label(root, text=s.get_info())
    l.place(x=300, y=300, anchor="center")


# 3学生选项
def ketangx2pg():
    global root2
    root38 = Tk()

    root38.title("Student")
    root38.geometry("640x480")
    root38.resizable(width=True, height=True)
    # 标签
    L_title = Label(root38, text='Please select')
    L_title.config(font='Helvetica -15 bold', fg='blue')
    L_title.place(x=60, y=10, anchor="center")
    # 创建学生
    B_11 = Button(root38, text="Create Student", command=chuangjiansxpg)
    B_11.place(x=40, y=60)
    # 管理学生
    B_12 = Button(root38, text="Manage Student", command=ketangx3pg)
    B_12.place(x=40, y=120)
    root38.mainloop()


# Add student to classroom
def chuangjiansxpg():
    global root46
    root46 = Tk()
    root46.title("Add student")
    root46.geometry("480x640")
    root46.resizable(width=True, height=True)
    # 学生添加
    L_title = Label(root46, text='Create student')
    L_title.config(font='Helvetica -15 bold', fg='blue')
    L_title.place(x=70, y=10, anchor="center")
    # 名字
    L_title = Label(root46, text='First name')
    L_title.config(font='Helvetica -15 bold', fg='red')
    L_title.place(x=50, y=50, anchor="center")
    # 输入按钮
    name = Entry(root46)
    # 输入框赋值在name变量
    name.pack(padx=100, pady=30)
    # 姓字
    L_title = Label(root46, text='Last name')
    L_title.config(font='Helvetica -15 bold', fg='red')
    L_title.place(x=50, y=100, anchor="center")
    # 输入按钮
    e2 = Entry(root46)
    # 输入框赋值在e变量
    e2.pack(padx=100, pady=5)
    # 性别
    L_title = Label(root46, text='Gender')
    L_title.config(font='Helvetica -15 bold', fg='red')
    L_title.place(x=50, y=150, anchor="center")
    # 输入按钮
    e3 = Entry(root46)
    # 输入框赋值在e变量
    e3.pack(padx=100, pady=30)
    # 学生号
    L_title = Label(root46, text='Student Number')
    L_title.config(font='Helvetica -15 bold', fg='red')
    L_title.place(x=80, y=200, anchor="center")
    # 输入按钮
    e4 = Entry(root46)
    # 输入框赋值在e变量
    e4.pack(padx=100, pady=1)
    # 年级
    L_title = Label(root46, text='Grade')
    L_title.config(font='Helvetica -15 bold', fg='red')
    L_title.place(x=50, y=250, anchor="center")
    # 输入按钮
    e5 = Entry(root46)
    # 输入框赋值在e变量
    e5.pack(padx=100, pady=25)
    # 邮箱
    L_title = Label(root46, text='Email')
    L_title.config(font='Helvetica -15 bold', fg='red')
    L_title.place(x=50, y=300, anchor="center")
    # 输入按钮
    e6 = Entry(root46)
    # 输入框赋值在e变量
    e6.pack(padx=100, pady=5)
    # 评论
    L_title = Label(root46, text='Comments')
    L_title.config(font='Helvetica -15 bold', fg='red')
    L_title.place(x=50, y=350, anchor="center")
    # 输入按钮
    e7 = Entry(root46)
    # 输入框赋值在e变量
    e7.pack(padx=100, pady=25)

    # 继续返回按钮
    B_15 = Button(root46, text="Next", command=lambda: [ghi(name.get(), e2.get(),
                                                            e3.get(), e4.get(),
                                                            e5.get(), e6.get(),
                                                            e7.get())])
    B_15.place(x=300, y=450)
    root46.mainloop()


def ghi(name, a, b, c, d, e, f):
    global school_students

    new_student = Student(name, a, b, c, d, e, f, "")
    school_students.append(new_student)
    chuangjian1cgpg()


# Class student info
def ketangxsxspg(c):
    root36 = Tk()

    root36.title("class student info")
    root36.geometry("640x480")
    root36.resizable(width=True, height=True)
    # 管理学生
    L_title = Label(root36, text="Student List")
    L_title.config(font='Helvetica -15 bold', fg='blue')
    L_title.place(x=150, y=20, anchor="center")
    t = c.student_list
    i = 0
    for s in t:
        l = Label(root36, text=s.get_info())
        l.place(x=150, y=50 + 30 * i, anchor="center")
        i += 1


# 4学生信息
def xsxxipg():
    global root2
    root69 = Tk()

    root69.title("Student Info")
    root69.geometry("640x480")
    root69.resizable(width=True, height=True)
    # 标签
    L_title = Label(root69, text='Student Info')
    L_title.config(font='Helvetica -15 bold', fg='blue')
    L_title.place(x=60, y=10, anchor="center")

    print(school_students)

    i = 0
    for s in school_students:
        l = Label(root69, text=s.get_info())
        l.place(x=150, y=50 + 30 * i, anchor="center")
        i += 1


# Login password
def denglumima():
    myAccount = a_entry.get()
    myPassword = p_entry.get()
    a_len = len(myAccount)
    p_len = len(myPassword)
    if myAccount == "a" and myPassword == "a":
        msg_label["text"] = "Successful Login"
        xuanxiang1pg()
    elif myAccount == "a" and myPassword != "a":
        msg_label["text"] = "password error"
        p_entry.delete(0, p_len)
    else:
        msg_label["text"] = "name error"
        a_entry.delete(0, a_len)
        p_entry.delete(0, p_len)


if __name__ == "__main__":
    # Initialization
    root = Tk()
    root.geometry("320x240")
    # name
    a_label = Label(root, text="Username:")
    a_label.grid(row=0, column=0, sticky=W)
    a_entry = Entry(root)
    a_entry.grid(row=0, column=1, sticky=E)
    # password
    p_label = Label(root, text="Password:")
    p_label.grid(row=1, column=0, sticky=W)
    p_entry = Entry(root)
    p_entry["show"] = "*"
    p_entry.grid(row=1, column=1, sticky=E)
    # log in button
    btn = Button(root, text="login", command=denglumima)
    btn.grid(row=2, column=1, sticky=E)
    # prompt
    msg_label = Label(root, text="")
    msg_label.grid(row=3)

    school_classes = []
    school_students = []
    root.mainloop()
