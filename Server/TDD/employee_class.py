class Trainer: 
    def __init__(self, emp_id, emp_name, courses_ongoing, courses_completed):
        self._emp_id = emp_id 
        self._emp_name = emp_name 
        self._courses_ongoing = courses_ongoing
        self._courses_completed = courses_completed

    def get_ongoing_courses_trainer(self):
        return self._courses_ongoing

    def get_completed_courses_trainer(self):
        return self._courses_completed
    
    def get_employee_status_trainer(self):
        return self._emp_id
        

class Learner: 
    def __init__(self, emp_id, emp_name, courses_ongoing, courses_completed):
        self._emp_id = emp_id 
        self._emp_name = emp_name 
        self._courses_ongoing = courses_ongoing
        self._courses_completed = courses_completed

    def get_completed_courses_learner(self):
        return self._courses_completed
    
    def get_employee_status_learner(self):
        return self._emp_id
    