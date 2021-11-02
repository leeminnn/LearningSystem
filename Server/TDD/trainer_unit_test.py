import unittest 
from trainer_class import Trainer
from trainer_class import Learner

class TestTrainer(unittest.TestCase): 

    def test_ongoing_courses_trainer(self):
        Joey = Trainer(1, "Joey", [2,3,4], [5,6], "")
        self.assertEqual(Joey.get_ongoing_courses_trainer(), [2,3,4])

    def test_completed_courses_trainer(self):
        Joy = Trainer(1, "Joy", [1,2], [7,8], "")
        self.assertEqual(Joy.get_completed_courses_trainer(), [7,8])

    def test_completed_courses_learner(self):
        Ken = Learner(1, "Ken", [5,6,2], [1,3],"")
        self.assertEqual(Ken.get_completed_courses_learner(), [1,3])        

    def test_employee_status_trainer(self):
        Peter = Trainer(1, "Peter", [1,2], [7,8], "")
        self.assertEqual(Peter.get_employee_status_trainer('1'), "Trainer") 

    def test_employee_status_learner(self):
        Peter = Learner(1, "Peter", [1,2], [7,8], "")
        self.assertEqual(Peter.get_employee_status_Learner('1'), 'Learner') 

    if __name__ == "__main__":
        unittest.main()