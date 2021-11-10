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

    def get_eligibility(self, course_required):
        if course_required in self._courses_completed:
            return self._emp_id
        else:
            raise Exception("Not eligible")


class Pending:
    def __init__(self, emp_id, emp_name, course_id, class_id, pending_status):
        self._emp_id = emp_id
        self._emp_name = emp_name
        self._course_id = course_id
        self._class_id = class_id
        self._pending_status = pending_status

    def get_pending(self):
        return self._emp_id
