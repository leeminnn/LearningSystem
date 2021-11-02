from datetime import datetime
class Class:
    def __init__(self,class_id,date,course_id):
        self.__class_id = class_id
        self.__date = date
        self.__course_id = course_id
        self.__classes = [{
            'class_id' : '02',
            'intake' : '40',
            'emp_id' : '03',
            'course_id': '115',
            'start_date':'2020-01-01',
            'end_date:' : '2020-03-03',
            'start_enrol':'2020-01-01',
            'end_enrol':'2020-03-03'
        },{
            'class_id' : '03',
            'intake' : '45',
            'emp_id' : '03',
            'course_id': '115',
            'start_date':'2020-01-01',
            'end_date:' : '2020-03-03',
            'start_enrol':'2021-01-01',
            'end_enrol':'2021-03-03'
        },{
            'class_id' : '06',
            'intake' : '30',
            'emp_id' : '03',
            'course_id': '115',
            'start_date':'2020-01-01',
            'end_date:' : '2022-01-01',
            'start_enrol':'2021-01-01',
            'end_enrol':'2021-12-12'
        },{
            'class_id' : '07',
            'intake' : '40',
            'emp_id' : '05',
            'course_id': '115',
            'start_date':'2020-01-01',
            'end_date:' : '2022-01-01',
            'start_enrol':'2021-01-01',
            'end_enrol':'2021-12-12'
        }]
    def get_class_on_period(self):
        class_list = []
        classes = self.__classes
        print(self.__date)
        date = self.__date
        for i in range(0,len(classes)):
            if classes[i]['course_id'] == self.__course_id:
                start_enrol = datetime.strptime(classes[i]['start_enrol'],'%Y-%m-%d').strftime('%Y-%m-%d')
                end_enrol = datetime.strptime (classes[i]['end_enrol'],'%Y-%m-%d').strftime('%Y-%m-%d')
                if (date >= start_enrol and date <= end_enrol):
                    class_list.append([classes[i]['class_id'],classes[i]['course_id'],classes[i]['intake']])
        return class_list