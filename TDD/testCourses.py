import unittest
from Server.Microservice.course.course import get_class_list
from course_class import Course
from class_class import Class
from datetime import date

class TestCourses(unittest.TestCase):
    def setUp(self):
        today = date.today()
        d1 = today.strftime("%Y-%m-%d")
        self.eligible_course = Course(['111'])
        self.completed_course = Course(['114'])
        self.inprogress_course = Course(['113','111'])
        self.incomplete_course = Course(['115'])
        self.class_on_period = Class("","113",d1)

    def tearDown(self):
        self.eligible_course = None
        self.completed_course = None
        self.inprogress_course = None
        self.incomplete_course = None
        self.class_on_period  = None
    
    def test_eligibleCourses(self):
        course = self.eligible_course.get_eligible_courses()
        self.assertEqual(course, [['111', 'WAD'],['113', 'ESD'],['115', 'STATS']])

    def test_completedCourses(self):
        course = self.completed_course.get_learner_courses()
        self.assertEqual(course, [['114', 'SPM']])

    def test_inprogressCourses(self):
        course = self.inprogress_course.get_learner_courses()
        self.assertEqual(course, [['113', 'ESD'],['111', 'WAD']])

    def test_incompleteCourses(self):
        course = self.incomplete_course.get_learner_courses()
        self.assertEqual(course, [['115', 'STATS']])
    
    def test_class_on_period(self):
        classes = self.class_on_period.get_class_on_period()
        self.assertEqual(classes,[])
    
if __name__ == "__main__":
    unittest.main()