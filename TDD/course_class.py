class Course:
    """"
    def __init__(self,course_id,course_name,course_desc,pre_req):
        self.course_id = course_id
        self.course_name = course_name
        self.course_desc = course_desc
        self.course_pre_req = pre_req
"""
    def __init__(self,course_id):
        self.__course_id = course_id
        self.__courses = [{
            'course_id' : '111',
            'course_name' : 'WAD',
            'course_description' : 'Web Application Development',
            'pre_req': ''
        },
        {
            'course_id' : '113',
            'course_name' : 'ESD',
            'course_description' : 'Enterprise Solution Development',
            'pre_req': '111'
        },{
            'course_id' : '114',
            'course_name' : 'SPM',
            'course_description' : 'Software Project Management',
            'pre_req': '113'
        },{
            'course_id' : '115',
            'course_name' : 'STATS',
            'course_description' : 'Introduction to Statistics',
            'pre_req': ''
        }
        ]

    def get_eligible_courses(self):
        eligible_course = []
        for j in range(0,len(self.__course_id)):
            for i in range(0,len(self.__courses)):
                if self.__courses[i]['pre_req'] == self.__course_id[j] or self.__courses[i]['pre_req'] == "":
                    eligible_course.append([self.__courses[i]['course_id'],self.__courses[i]['course_name']])
        return eligible_course

    def get_learner_courses(self):
        course_list = []
        for j in range(0,len(self.__course_id)):
            for i in range(0,len(self.__courses)):
                if self.__courses[i]['course_id'] == self.__course_id[j]:
                    course_list.append([self.__courses[i]['course_id'],self.__courses[i]['course_name']])
        return course_list
        

