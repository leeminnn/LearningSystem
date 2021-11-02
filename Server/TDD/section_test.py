import unittest
from section import Section

class TestSection(unittest.TestCase):

    # def setUp(self):
    #     self._section_id = section_id
    #     self._class_name = class_name
    #     self._course_name = course_name
    #     self._quiz_id = quiz_id
    #     self._section_name = section_name
    #     self._course_id = course_id
    #     self._class_id = class_id
    #     self._quiz_status = quiz_status 
    #     self._section_progress = section_progress


    # def tearDown(self):
    #     self._section_id = None
    #     self._class_name = None
    #     self._course_name = None
    #     self._quiz_id = None
    #     self._section_name = None
    #     self._course_id = None
    #     self._class_id = None
    #     self._quiz_status = None 
    #     self._section_progress = None


    def test_get_section_name(self): 
        section1 = Section('1', '1', "WAD", '1', 'Week 1', '1', '1', 'pass', '50')
        self.assertEqual(section1.get_section_name(), 'Week 1')


    def test_get_quiz(self): 
        section1 = Section('1', '1', "WAD", '1', 'Week 1', '1', '1', 'pass','50' )
        self.assertEqual(section1.get_quiz_id(), '1')

    
    def test_get_quiz_completion(self): 
        section1 = Section('1', '1', "WAD", '1', 'Week 1', '1', '1', 'pass','50')
        self.assertEqual(section1.get_quiz_completion(), 'pass')

    def test_get_section_progress(self): 
        section1 = Section('1', '1', "WAD", '1', 'Week 1', '1', '1', 'pass','50')
        self.assertEqual(section1.get_section_progress(), '50')

if __name__ == "__main__":
    unittest.main()
