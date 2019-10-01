
import unittest
import markbook
from markbook import Student, Assignment, Classroom
from selenium import webdriver
import unittest
# import time
# import HTMLTestRunner


class TestMarkbook(unittest.TestCase):

    def setUp(self):
        print("调用setup")

    def tearDown(self):
        print("清理")

    def test_Student(self):
        print("test_student_class")
        result = Student("Charlie", "Guo", "Male", "image", "12345", "12", "gmail", "Good")
        self.assertEqual(result.__str__(), "{0} {1} {2}".format("Charlie", "Guo", "12345"))
        print("test_student_average_of_course")
        result = Student("Charlie", "Guo", "Male", "image", "12345", "12", "gmail", "Good")
        self.assertEqual(result.get_assignment_average("ICS4U"), None)

    #     self.assertFalse(is_prime(1))
    #     self.assertTrue(is_prime(3))
    #     self.assertTrue(is_prime(2))
    #     self.assertFalse(is_prime(0))
    #
    # def test_add(self):
    #     print("add")
    #     self.assertEqual(3, add(1, 2))
    #     self.assertNotEqual(3, add(2, 2))
    #
    # def test_divide(self):
    #     print("divide")
    #     self.assertEqual(2, divide(6, 3))
    #     self.assertNotEqual(2, divide(6, 4))
    #
    # def test_insert(self):
    #     print("insert")
    #     # self.assertEqual([1, 2, 5, 3, 4], insert_at([1, 2, 3, 4], 5, 2))
    #     self.assertEqual([1, 2, 3, 5, 6], insert([1, 2, 5, 6], 3))
    #     self.assertEqual([0, 2, 3, 5, 6], insert([2, 3, 5, 6], 0))
    #     self.assertEqual([1, 2, 3, 5, 6], insert([1, 2, 3, 5], 6))
    #
    # def test_remove(self):
    #     print("remove")
    #     self.assertEqual([1, 3, 5, 9], remove([1, 3, 5, 7, 9], 7))
    #     self.assertFalse(False, remove([1, 3, 5], 6))

if __name__ == "__main__":
    # filepath = 'C:\\Intel\\htmlreport.html'
    # ftp = open(filepath, 'wb')
    # suite = unittest.TestSuite()
    # suite.addTest(TestGoodbye('test_case'))
    # runner = HTMLTestrunner.HTMLTestRunner(stream=ftp, title='welcome to this web')
    unittest.main()
# @pytest.mark.skip
# def test_create_assigment():
#     assignment1 = markbook.create_assignment(name="Assignment One",
#                                             due="2019-09-21",
#                                             points=100)
#     expected = {
#         "name": "Assignment One",
#         "due": "2019-09-21",
#         "points": 100
#     }
#     assert assignment1 == expected
#
#     assignment2 = markbook.create_assignment(name="Assignment Two",
#                                              due=None,
#                                              points=1)
#     assert assignment2["name"] == "Assignment Two"
#     assert assignment2["due"] is None
#     assert assignment2["points"] == 1
#
#
# @pytest.mark.skip()
# def test_create_classroom():
#     classroom = markbook.create_classroom(course_code="ICS4U",
#                                           course_name="Computer Science",
#                                           period=2,
#                                           teacher="Mr. Gallo")
#     expected = {
#         "course_code": "ICS4U",
#         "course_name": "Computer Science",
#         "period": 2,
#         "teacher": "Mr. Gallo"
#     }
#
#     # The classroom needs to be a dictionary identical to the expected
#     assert classroom == expected
#
#     # The classroom needs to be created with
#     # empty lists for students and assignments
#     assert classroom["student_list"] == []
#     assert classroom["assignment_list"] == []
#
#
# # @pytest.mark.skip
# def test_calculate_average_mark():
#     student = {
#         "marks": [50, 100]
#     }
#     assert markbook.calculate_average_mark(student) == 75.0
#
#
# #@pytest.mark.skip
# def test_add_student_to_classroom():
#     """
#     Dependencies:
#         - create_classroom()
#     """
#     classroom = markbook.create_classroom(course_code="ICS4U",
#                                           course_name="Computer Science",
#                                           period=2,
#                                           teacher="Mr. Gallo")
#     student = {"first_name": "John", "last_name": "Smith"}
#
#     assert len(classroom["student_list"]) == 0
#     markbook.add_student_to_classroom(student, classroom)
#     assert type(classroom["student_list"]) is list
#     assert len(classroom["student_list"]) == 1
#
#
# #@pytest.mark.skip
# def test_remove_student_from_classroom():
#     """
#     Dependencies:
#         - create_classroom()
#         - add_student_to_classroom()
#     """
#     classroom = markbook.create_classroom(course_code="ICS4U",
#                                           course_name="Computer Science",
#                                           period=2,
#                                           teacher="Mr. Gallo")
#     student = {"first_name": "John", "last_name": "Smith"}
#
#     markbook.add_student_to_classroom(student, classroom)
#     assert len(classroom["student_list"]) == 1
#     markbook.remove_student_from_classroom(student, classroom)
#     assert type(classroom["student_list"]) is list
#     assert len(classroom["student_list"]) == 0
#
#
# #@pytest.mark.skip
# def test_edit_student():
#     student = {"first_name": "John", "last_name": "Smith", "grade": 10}
#     markbook.edit_student(student, first_name="Frank", last_name="Bell")
#     assert student["first_name"] == "Frank"
#     assert student["last_name"] == "Bell"
#     assert student["grade"] == 10
