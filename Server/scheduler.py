import schedule
import time
import requests
import json
import os
import subprocess

def run_python():
    os.system("echo cd Server")
    os.system("echo cd Server/Microservice/course")
    os.system("echo python course.py & python employee.py") 
    #os.system("echo python employee.py") 
    #subprocess.run("python course.py & python employee.py", shell=True)
    get_courses()

def get_courses():
    url = "http://localhost:5000/ended_classes"
    page=requests.get(url)
    data = page.json()
    #
    for i in data:
        print(i)
        get_class_list(i['course_id'],i['class_id'])

def get_class_list(course_id,class_id):
    url = "http://localhost:5000/check_class_list/"+ str(class_id)
    page = requests.get(url)
    data = page.json()
    for i in data:
        if (i['progress'] != 100 and i['graded_result'] != 'Pass' and i['class_status'] !='Completed'):
            url = "http://localhost:5001/update_to_incomplete"
            emp_id = i['emp_id']
            course_id = i['course_id']
            dummy = json.dumps({"emp_id": str(emp_id),"course_id":str(course_id)})
            headers = {
                "Content-Type": "application/json",
                'Accept':'application/json'
            }
            page = requests.put("http://localhost:5001/update_to_incomplete",data=dummy,headers=headers, verify=False)
            data = page.text
            print(data)

    
schedule.every().day.at("00:00").do(run_python())
#schedule.every(20).seconds.do(run_python)
#schedule.every(10).seconds.do(do_nothing)

while True:
    schedule.run_pending()
    time.sleep(1)