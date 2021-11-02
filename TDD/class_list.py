class ClassList:
    def __init__(self,class_id,emp_id):
        self.__class_id = class_id
        self.__emp_id = emp_id

        self.__classes_list = [{
            'emp_id' : '01',
            'class_id' : '01',
            'progress' : '25',
            'class_status': 'Ongoing',
            'ungraded_result':'1,0,0,0'
        },{
            'emp_id' : '02',
            'class_id' : '01',
            'progress' : '50',
            'class_status': 'Ongoing',
            'ungraded_result':'1,1,0,0'
        },{
            'emp_id' : '05',
            'class_id' : '03',
            'progress' : '100',
            'class_status': 'Ongoing',
            'ungraded_result':'1,1,1'
        },{
            'emp_id' : '08',
            'class_id' : '03',
            'progress' : '0',
            'class_status': 'Ongoing',
            'ungraded_result':'0,0,0'
        }]

    def get_class_list(self):
        class_list = []
        for i in range(0,len(self.__classes_list)):
            if self.__classes_list[i]['class_id'] == self.__class_id:
                class_list.append([self.__classes_list[i]['emp_id'],self.__classes_list[i]['progress'],self.__classes_list[i]['ungraded_result']])
        return class_list

    def get_progess(self):
        for i in range(0,len(self.__classes_list)):
            if self.__classes_list[i]['class_id'] == self.__class_id:
                if self.__classes_list[i]['emp_id'] == self.__emp_id:
                    return self.__classes_list[i]['progress']