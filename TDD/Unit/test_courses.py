import unittest
from course_unit_class import Class, ClassList, Course
from datetime import datetime


class TestCourses(unittest.TestCase):
    def setUp(self):
        today = datetime.today().strftime('%Y-%m-%d')
        self.eligible_course = Course(['111'])
        self.completed_course = Course(['114'])
        self.inprogress_course = Course(['113', '111'])
        self.incomplete_course = Course(['115'])
        self.class_on_period = Class("", today, "115")
        self.class_list = ClassList("01", "")
        self.progress = ClassList("03", "05")

    def tearDown(self):
        self.eligible_course = None
        self.completed_course = None
        self.inprogress_course = None
        self.incomplete_course = None
        self.class_on_period = None
        self.class_list = None
        self.progress = None

    def test_eligibleCourses(self):
        course = self.eligible_course.get_eligible_courses()
        self.assertEqual(
            course, [['111', 'WAD'], ['113', 'ESD'], ['115', 'STATS']])

    def test_completedCourses(self):
        course = self.completed_course.get_learner_courses()
        self.assertEqual(course, [['114', 'SPM']])

    def test_inprogressCourses(self):
        course = self.inprogress_course.get_learner_courses()
        self.assertEqual(course, [['113', 'ESD'], ['111', 'WAD']])

    def test_incompleteCourses(self):
        course = self.incomplete_course.get_learner_courses()
        self.assertEqual(course, [['115', 'STATS']])

    def test_classList(self):
        course = self.class_list.get_class_list()
        self.assertEqual(
            course, [['01', '25', '1,0,0,0'], ['02', '50', '1,1,0,0']])

    def test_progress(self):
        course = self.progress.get_progess()
        self.assertEqual(course, '100')

    def test_class_on_period(self):
        classes = self.class_on_period.get_class_on_period()
        self.assertEqual(classes, [['06', '115', '30'], ['07', '115', '40']])


if __name__ == "__main__":
    unittest.main()
