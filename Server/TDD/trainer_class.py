class Trainer: 
    def __init__(self, emp_id, emp_name, courses_ongoing, courses_completed, emp_status):
        self._emp_id = emp_id 
        self._emp_name = emp_name 
        self._courses_ongoing = courses_ongoing
        self._courses_completed = courses_completed
        self._emp_status = emp_status

    def get_ongoing_courses_trainer(self):
        return self._courses_ongoing

    def get_completed_courses_trainer(self):
        return self._courses_completed
    
    def get_employee_status_trainer(self, employee_id):
        if employee_id == self._emp_id:
            self._emp_status = "Trainer"
            return self._emp_status
        

class Learner: 
    def __init__(self, emp_id, emp_name, courses_ongoing, courses_completed, emp_status):
        self._emp_id = emp_id 
        self._emp_name = emp_name 
        self._courses_ongoing = courses_ongoing
        self._courses_completed = courses_completed
        self._emp_status = emp_status

    def get_completed_courses_learner(self):
        return self._courses_completed
    
    def get_employee_status_learner(self, employee_id):
        if self._emp_id == employee_id:
            self._emp_status = 'Learner'
            return self._emp_status
    