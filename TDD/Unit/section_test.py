import unittest
from section_unit_class import Section


class TestSection(unittest.TestCase):

    def test_get_section_name(self):
        section1 = Section('1', '1', "WAD", '1', 'Week 1',
                           '1', '1', 'pass', '50')
        self.assertEqual(section1.get_section_name(), 'Week 1')

    def test_get_quiz(self):
        section1 = Section('1', '1', "WAD", '1', 'Week 1',
                           '1', '1', 'pass', '50')
        self.assertEqual(section1.get_quiz_id(), '1')

    def test_get_quiz_completion(self):
        section1 = Section('1', '1', "WAD", '1', 'Week 1',
                           '1', '1', 'pass', '50')
        self.assertEqual(section1.get_quiz_completion(), 'pass')

    def test_get_section_progress(self):
        section1 = Section('1', '1', "WAD", '1', 'Week 1',
                           '1', '1', 'pass', '50')
        self.assertEqual(section1.get_section_progress(), '50')


if __name__ == "__main__":
    unittest.main()
