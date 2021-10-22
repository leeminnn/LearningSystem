import requests
import datetime
from flask import jsonify, Flask, request
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app)

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3305
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'employee'

mysql = MySQL(app, cursorclass=DictCursor)
mysql.init_app(app)

#get list all employees
@app.route("/all_employee", methods=['POST']) 
def all_employee():

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""SELECT * FROM employee.employee""")
    result = cur.fetchall()

    return jsonify(result), 200

#get all information of 1 employee
@app.route("/get_one", methods=['POST'])
def get_one():
                # check for body request
    if not request.json:
        return("Invalid body request."), 400

    emp_id = request.json['emp_id']

    conn = mysql.connect()
    cur = conn.cursor()

    cur.execute("""SELECT * FROM employee.employee WHERE emp_id=%s""", (emp_id))

    result = cur.fetchall()
    conn.commit()
    cur.close()


    return jsonify(result), 200

#get employee name when type id
@app.route("/get_emp_name", methods=['POST'])
def get_emp_name():
                # check for body request
    if not request.json:
        return("Invalid body request."), 400

    emp_id = request.json['emp_id']

    conn = mysql.connect()
    cur = conn.cursor()

    cur.execute("""SELECT emp_id,emp_name FROM employee.employee WHERE emp_id=%s""", (emp_id))

    result = cur.fetchall()
    conn.commit()
    cur.close()


    return jsonify(result), 200

#get all trainers id name
@app.route("/get_trainers", methods=['POST'])
def get_trainers():

    conn = mysql.connect()
    cur = conn.cursor()

    cur.execute("""SELECT emp_id,emp_name FROM employee.trainer""")

    result = cur.fetchall()
    conn.commit()
    cur.close()


    return jsonify(result), 200


#update employee information
@app.route('/update_employee', methods=['PUT']) 
def update_employee():
    #check for body request
    if not request.json:
        return ("Invalid body request."),400

    emp_id = request.json['emp_id']
    emp_name = request.json['emp_name']
    email = request.json['email']
    phone = request.json['phone']
    dept = request.json['dept']

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""UPDATE employee.employee SET emp_name = %s, email = %s , phone =%s, dept=%s
                WHERE emp_id = %s """,
                (emp_name, email, phone, dept,emp_id))

    # commit the command
    conn.commit()

    # close sql connection
    cur.close()

    return("Successfully Update employee information"), 200

#add new employee
@app.route('/add_employee', methods=['POST']) 
def add_employee():
    #check for body request
    if not request.json:
        return("Invalid body request."), 400
    
    emp_id = request.json['emp_id']
    emp_name = request.json['emp_name']
    email = request.json['email']
    phone = request.json['phone']
    dept = request.json['dept']

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""INSERT INTO employee.employee(emp_id,emp_name,email,phone,dept) VALUES (%s, %s, %s, %s, %s)""",
                (emp_id,emp_name,email,phone,dept))    
    # commit the command
    conn.commit()

    # close sql connection
    cur.close()

    return("Successfully added employee"), 200

#insert new trainer
@app.route('/add_trainer', methods=['POST']) 
def add_trainer():
    #check for body request
    if not request.json:
        return("Invalid body request."), 400
    
    emp_id = request.json['emp_id']
    emp_name = request.json['emp_name']
    courses_teaching = request.json['courses_teaching']
    courses_completed = request.json['courses_completed']

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""INSERT INTO employee.trainer(emp_id,emp_name,courses_teaching,courses_completed) VALUES (%s, %s, %s, %s)""",
                (emp_id,emp_name,courses_teaching,courses_completed))    
    # commit the command
    conn.commit()

    # close sql connection
    cur.close()
    return("Successfully add new trainer"), 200

#update trainer courses teaching
@app.route('/update_trainer_teaching', methods=['PUT']) 
def update_trainer_teaching():
    #check for body request
    if not request.json:
        return("Invalid body request."), 400
    
    emp_id = request.json['emp_id']
    courses_teaching = request.json['courses_teaching']

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""UPDATE employee.trainer SET courses_teaching = %s
                WHERE emp_id = %s """,
                (courses_teaching,emp_id)) 
    # commit the command
    conn.commit()

    # close sql connection
    cur.close()

    return("Successfully update courses teaching"), 200

#update trainer courses completed
@app.route('/update_trainer_completed', methods=['PUT']) 
def update_trainer_completed():
    #check for body request
    if not request.json:
        return("Invalid body request."), 400
    
    emp_id = request.json['emp_id']
    courses_completed = request.json['courses_completed']

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""UPDATE employee.trainer SET courses_completed = %s
                WHERE emp_id = %s """,
                (courses_completed,emp_id)) 
    # commit the command
    conn.commit()

    # close sql connection
    cur.close()

    return("Successfully update courses completed"), 200

#insert new learner
@app.route('/add_learner', methods=['POST']) 
def add_learner():
    #check for body request
    if not request.json:
        return("Invalid body request."), 400
    
    emp_id = request.json['emp_id']
    emp_name = request.json['emp_name']
    courses_ongoing = request.json['courses_ongoing']
    courses_completed = request.json['courses_completed']
    badge=request.json['badge']

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""INSERT INTO employee.learner(emp_id,emp_name,courses_ongoing,courses_completed,badge) VALUES (%s, %s, %s, %s,%s)""",
                (emp_id,emp_name,courses_ongoing,courses_completed,badge))    
    # commit the command
    conn.commit()

    # close sql connection
    cur.close()
    return("Successfully add new learner"), 200

#update learner courses_ongoing
@app.route('/update_learner_ongoing', methods=['PUT']) 
def update_learner_ongoing():
    #check for body request
    if not request.json:
        return("Invalid body request."), 400
    
    emp_id = request.json['emp_id']
    courses_ongoing = request.json['courses_ongoing']

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""UPDATE employee.learner SET courses_ongoing = %s
                WHERE emp_id = %s """,
                (courses_ongoing,emp_id)) 
    # commit the command
    conn.commit()

    # close sql connection
    cur.close()

    return("Successfully update ongoing courses"), 200

#update learner courses_completed
@app.route('/update_learner_completed', methods=['PUT']) 
def update_learner_completed():
    #check for body request
    if not request.json:
        return("Invalid body request."), 400
    
    emp_id = request.json['emp_id']
    courses_completed = request.json['courses_completed']

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""UPDATE employee.learner SET courses_completed = %s
                WHERE emp_id = %s """,
                (courses_completed,emp_id)) 
    # commit the command
    conn.commit()

    # close sql connection
    cur.close()

    return("Successfully update completed courses"), 200

#update learner courses_badge
@app.route('/update_learner_badge', methods=['PUT']) 
def update_learner_badge():
    #check for body request
    if not request.json:
        return("Invalid body request."), 400
    
    emp_id = request.json['emp_id']
    badge = request.json['badge']

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""UPDATE employee.learner SET badge = %s
                WHERE emp_id = %s """,
                (badge,emp_id)) 
    # commit the command
    conn.commit()

    # close sql connection
    cur.close()

    return("Successfully update learner badge"), 200

#get trainer courses teaching
@app.route("/get_courses_teaching", methods=['POST'])
def get_courses_teaching():
    # check for body request
    if not request.json:
        return("Invalid body request."), 400

    emp_id = request.json['emp_id']

    conn = mysql.connect()
    cur = conn.cursor()

    cur.execute("""SELECT courses_teaching FROM employee.trainer where emp_id=%s""",(emp_id))

    result = cur.fetchall()
    conn.commit()
    cur.close()


    return jsonify(result), 200

#get trainer completed courses
@app.route("/get_trainer_courses_completed", methods=['POST'])
def get_trainer_courses_completed():
    # check for body request
    if not request.json:
        return("Invalid body request."), 400

    emp_id = request.json['emp_id']

    conn = mysql.connect()
    cur = conn.cursor()

    cur.execute("""SELECT courses_completed FROM employee.trainer where emp_id=%s""",(emp_id))

    result = cur.fetchall()
    conn.commit()
    cur.close()


    return jsonify(result), 200

#get learner ongoing courses
@app.route("/get_courses_ongoing", methods=['POST'])
def get_courses_ongoing():
    # check for body request
    if not request.json:
        return("Invalid body request."), 400

    emp_id = request.json['emp_id']

    conn = mysql.connect()
    cur = conn.cursor()

    cur.execute("""SELECT courses_ongoing FROM employee.learner where emp_id=%s""",(emp_id))

    result = cur.fetchall()
    conn.commit()
    cur.close()


    return jsonify(result), 200

#get learner completed courses
@app.route("/get_learner_courses_completed", methods=['POST'])
def get_learner_courses_completed():
    # check for body request
    if not request.json:
        return("Invalid body request."), 400

    emp_id = request.json['emp_id']

    conn = mysql.connect()
    cur = conn.cursor()

    cur.execute("""SELECT courses_completed FROM employee.learner where emp_id=%s""",(emp_id))

    result = cur.fetchall()
    conn.commit()
    cur.close()


    return jsonify(result), 200


#learner completed courses 
@app.route("/learner_completed_courses", methods=['POST'])
def learner_completed_courses(course_id):
            # check for body request
    if not request.json:
        return("Invalid body request."), 400

    conn = mysql.connect()
    cur = conn.cursor()
    # cur.execute("""SELECT course.course_id,course.course_name,course_desc,class.class_id,class_name,class.emp_name "trainer_name",class.emp_id "trainer_id"
    #             FROM course.course AS course 
    #             INNER JOIN course.class AS class 
    #             ON course.course_id = class.course_id
    #             INNER JOIN course.class_list AS class_list
    #             ON class.class_id = class_list.class_id
    #             WHERE course.course_id IN %s""" ,[tuple(course_id)])

    cur.execute("""SELECT * FROM course.course WHERE course_id IN %s""" ,[tuple(course_id)])    
    result = cur.fetchall()
    res = requests.post("http://192.168.0.142:5000/get_learner_courses_completed", result).json()
    conn.commit()
    cur.close()


    return jsonify(res), 200

#learner inprogress courses 
@app.route("/learner_inprogress_courses", methods=['POST'])
def learner_inprogress_courses(course_id):
            # check for body request
    if not request.json:
        return("Invalid body request."), 400


    conn = mysql.connect()
    cur = conn.cursor()
    # cur.execute("""SELECT course.course_id,course.course_name,course_desc,class.class_id,class_name,class.emp_name "trainer_name",class.emp_id "trainer_id"
    #             FROM course.course AS course 
    #             INNER JOIN course.class AS class 
    #             ON course.course_id = class.course_id
    #             INNER JOIN course.class_list AS class_list
    #             ON class.class_id = class_list.class_id
    #             WHERE course.course_id IN %s""" ,[tuple(course_id)])

    cur.execute("""SELECT * FROM course.course WHERE course_id IN %s""" ,[tuple(course_id)])
    result = cur.fetchall()
    res = requests.post("http://192.168.0.142:5000/get_inprogress_course/<string:course_id>", result).json()
    conn.commit()
    cur.close()


    return jsonify(res), 200


#learner eligible courses 
@app.route("/learner_eligible_courses", methods=['POST'])
def learner_eligible_courses(course_id):
            # check for body request
    if not request.json:
        return("Invalid body request."), 400

    conn = mysql.connect()
    cur = conn.cursor()
    if course_id == []:
        cur.execute("""SELECT * FROM course.course WHERE pre_req IS NULL""")
    else:
        cur.execute("""SELECT * FROM course.course WHERE pre_req IN %s OR pre_req IS NULL""" ,[tuple(course_id)])    
        result = cur.fetchall()

    res = requests.post("http://192.168.0.142:5000/get_learner_eligible_courses/<string:course_id>", result).json()
    conn.commit()
    cur.close()


    return jsonify(res), 200

#trainer inprogress courses 
@app.route("/trainer_inprogress_courses", methods=['POST'])
def trainer_inprogress_courses(course_id):
            # check for body request
    if not request.json:
        return("Invalid body request."), 400

    conn = mysql.connect()
    cur = conn.cursor()
    #cur.execute("""SELECT course.course_id,course.course_name,course_desc,class.class_id,class_name,start_date,end_date,emp_name,emp_id
                #FROM course.course AS course 
               # INNER JOIN course.class AS class 
               # ON course.course_id = class.course_id
              #  WHERE course.course_id IN %s""" ,[tuple(course_id)])
    
    cur.execute("""SELECT * FROM course.course WHERE course_id IN %s""" ,[tuple(course_id)])

    result = cur.fetchall()
    res = requests.post("http://192.168.0.142:5000/get_trainer_ongoing_courses/<string:course_id>", result).json()
    conn.commit()
    cur.close()


    return jsonify(res), 200

#trainer completed courses 
@app.route("/trainer_completed_courses", methods=['POST'])
def trainer_completed_courses(course_id):
            # check for body request
    if not request.json:
        return("Invalid body request."), 400

    conn = mysql.connect()
    cur = conn.cursor()
    #cur.execute("""SELECT course.course_id,course.course_name,course_desc,class.class_id,class_name,start_date,end_date,emp_name,emp_id
                #FROM course.course AS course 
               # INNER JOIN course.class AS class 
                #ON course.course_id = class.course_id
                #WHERE course.course_id IN %s""" ,[tuple(course_id)])
    cur.execute("""SELECT * FROM course.course WHERE course_id IN %s""" ,[tuple(course_id)])

    result = cur.fetchall()
    res = requests.post("http://192.168.0.142:5000/get_trainer_completed_courses/<string:course_id>", result).json()
    conn.commit()
    cur.close()


    return jsonify(res), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
