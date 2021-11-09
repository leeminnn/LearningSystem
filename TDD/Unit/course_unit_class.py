from datetime import datetime


class Class:
    def __init__(self, class_id, date, course_id):
        self.__class_id = class_id
        self.__date = date
        self.__course_id = course_id
        self.__classes = [{
            'class_id': '02',
            'intake': '40',
            'emp_id': '03',
            'course_id': '115',
            'start_date': '2020-01-01',
            'end_date:': '2020-03-03',
            'start_enrol': '2020-01-01',
            'end_enrol': '2020-03-03'
        }, {
            'class_id': '03',
            'intake': '45',
            'emp_id': '03',
            'course_id': '115',
            'start_date': '2020-01-01',
            'end_date:': '2020-03-03',
            'start_enrol': '2021-01-01',
            'end_enrol': '2021-03-03'
        }, {
            'class_id': '06',
            'intake': '30',
            'emp_id': '03',
            'course_id': '115',
            'start_date': '2020-01-01',
            'end_date:': '2022-01-01',
            'start_enrol': '2021-01-01',
            'end_enrol': '2021-12-12'
        }, {
            'class_id': '07',
            'intake': '40',
            'emp_id': '05',
            'course_id': '115',
            'start_date': '2020-01-01',
            'end_date:': '2022-01-01',
            'start_enrol': '2021-01-01',
            'end_enrol': '2021-12-12'
        }]

    def get_class_on_period(self):
        class_list = []
        classes = self.__classes
        print(self.__date)
        date = self.__date
        for i in range(0, len(classes)):
            if classes[i]['course_id'] == self.__course_id:
                start_enrol = datetime.strptime(
                    classes[i]['start_enrol'], '%Y-%m-%d').strftime('%Y-%m-%d')
                end_enrol = datetime.strptime(
                    classes[i]['end_enrol'], '%Y-%m-%d').strftime('%Y-%m-%d')
                if (date >= start_enrol and date <= end_enrol):
                    class_list.append(
                        [classes[i]['class_id'], classes[i]['course_id'], classes[i]['intake']])
        return class_list


class ClassList:
    def __init__(self, class_id, emp_id):
        self.__class_id = class_id
        self.__emp_id = emp_id

        self.__classes_list = [{
            'emp_id': '01',
            'class_id': '01',
            'progress': '25',
            'class_status': 'Ongoing',
            'ungraded_result': '1,0,0,0'
        }, {
            'emp_id': '02',
            'class_id': '01',
            'progress': '50',
            'class_status': 'Ongoing',
            'ungraded_result': '1,1,0,0'
        }, {
            'emp_id': '05',
            'class_id': '03',
            'progress': '100',
            'class_status': 'Ongoing',
            'ungraded_result': '1,1,1'
        }, {
            'emp_id': '08',
            'class_id': '03',
            'progress': '0',
            'class_status': 'Ongoing',
            'ungraded_result': '0,0,0'
        }]

    def get_class_list(self):
        class_list = []
        for i in range(0, len(self.__classes_list)):
            if self.__classes_list[i]['class_id'] == self.__class_id:
                class_list.append([self.__classes_list[i]['emp_id'], self.__classes_list[i]
                                  ['progress'], self.__classes_list[i]['ungraded_result']])
        return class_list

    def get_progess(self):
        for i in range(0, len(self.__classes_list)):
            if self.__classes_list[i]['class_id'] == self.__class_id:
                if self.__classes_list[i]['emp_id'] == self.__emp_id:
                    return self.__classes_list[i]['progress']


class Course:

    def __init__(self, course_id):
        self.__course_id = course_id
        self.__courses = [{
            'course_id': '111',
            'course_name': 'WAD',
            'course_description': 'Web Application Development',
            'pre_req': ''
        },
            {
            'course_id': '113',
            'course_name': 'ESD',
            'course_description': 'Enterprise Solution Development',
            'pre_req': '111'
        }, {
            'course_id': '114',
            'course_name': 'SPM',
            'course_description': 'Software Project Management',
            'pre_req': '113'
        }, {
            'course_id': '115',
            'course_name': 'STATS',
            'course_description': 'Introduction to Statistics',
            'pre_req': ''
        }
        ]

    def get_eligible_courses(self):
        eligible_course = []
        for j in range(0, len(self.__course_id)):
            for i in range(0, len(self.__courses)):
                if self.__courses[i]['pre_req'] == self.__course_id[j] or self.__courses[i]['pre_req'] == "":
                    eligible_course.append(
                        [self.__courses[i]['course_id'], self.__courses[i]['course_name']])
        return eligible_course

    def get_learner_courses(self):
        course_list = []
        for j in range(0, len(self.__course_id)):
            for i in range(0, len(self.__courses)):
                if self.__courses[i]['course_id'] == self.__course_id[j]:
                    course_list.append(
                        [self.__courses[i]['course_id'], self.__courses[i]['course_name']])
        return course_list
