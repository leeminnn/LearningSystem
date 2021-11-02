        #Test Get section ids and name of the specific class and course
        #Test get section ids of specific class and course based on progress
        #Test Final Quiz Completion - Reflect Pass/Fail
        #Test get quiz id and name of the specific section id , course id and class id

class Section:

    def __init__(self, section_id, class_name, course_name, quiz_id, section_name, course_id, class_id, quiz_status, section_progress):
        self._section_id = section_id
        self._class_name = class_name
        self._course_name = course_name
        self._quiz_id = quiz_id
        self._section_name = section_name
        self._course_id = course_id
        self._class_id = class_id
        self._quiz_status = quiz_status 
        self._section_progress = section_progress

    def get_section_id(self): 
        return self._section_id

    def get_section_name(self): 
        return self._section_name
    
    def get_section_progress(self): 
        return self._section_progress

    def get_quiz_completion(self):
        return self._quiz_status
    
    def get_quiz_id(self): 
        return self._quiz_id

    def get_course_id(self): 
        return self._course_id

    def get_course_name(self): 
        return self._course_name

    def get_class_id(self): 
        return self._class_id

    def get_class_name(self): 
        return self._class_name



        

