import requests
import datetime
from flask import jsonify, Flask, request
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3305
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'course'

mysql = MySQL(app, cursorclass=DictCursor)
mysql.init_app(app)


#HR create new course
@app.route('/create_course', methods=['POST']) 
def create_course():

    # check for body request
    if not request.json:
        return("Invalid body request."), 400

    course_id = request.json['course_id']
    course_name = request.json['course_name']
    start_date = request.json['start_date']
    end_date = request.json['end_date']
    pre_requisite = request.json['pre_requisite']

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""INSERT INTO course.course(course_id, course_name, start_date,end_date,pre_req) VALUES (%s, %s, %s, %s, %s)""",
                (course_id, course_name, start_date, end_date, pre_requisite))

    # commit the command
    conn.commit()

    # close sql connection
    cur.close()

    return("Successfully Create Course"), 201

#HR Create new class to assign trainers after creating a new course
@app.route('/create_class', methods=['POST']) 
def create_class():
    #check for body request
    if not request.json:
        return("Invalid body request."), 400
    
    course_id = request.json['course_id'];
    class_id = request.json['class_id'];
    class_name= request.json['class_name'];
    intake = request.json['intake'];
    emp_id = request.json['emp_id'];

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""INSERT INTO course.class(class_id,class_name,intake,emp_id,course_id) VALUES (%s, %s, %s, %s, %s)""",
                (class_id,class_name,intake,emp_id,course_id))    # commit the command
    conn.commit()

    # close sql connection
    cur.close()

    return("Successfully Create Class"), 201
    

#HR update course
@app.route('/update_course', methods=['PUT']) 
def update_class():
    #check for body request
    if not request.json:
        return ("Invalid body request."),400

    course_id = request.json['course_id']
    course_name = request.json['course_name']
    start_date = request.json['start_date']
    end_date = request.json['end_date']
    pre_requisite = request.json['pre_requisite']

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""UPDATE course.course SET course_name = %s, start_date = %s , end_date =%s, pre_req=%s
                WHERE course_id = %s """,
                (course_name, start_date, end_date, pre_requisite,course_id))

    # commit the command
    conn.commit()

    # close sql connection
    cur.close()

    return("Successfully Update Course"), 201

@app.route("/all_courses", methods=['GET']) 
def all_courses():

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM course.course")
    result = cur.fetchall()

    return jsonify(result), 203

## learner want to enroll to the course ##
@app.route('/enrol', methods=['POST']) 
def enrol():

    # check for body request
    if not request.json:
        return("Invalid body request."), 400

    # request --> getting data that is being sent over
    # json --> convert file to json format
    emp_id = request.json['emp_id']
    course_id = request.json['course_id']
    class_id = request.json['class_id']
    status = request.json['status']

    # connect to sql
    conn = mysql.connect()
    cur = conn.cursor()

    # SQL command
    cur.execute("""INSERT INTO course.pending_enrolment(emp_id, course_id, class_id, status) VALUES (%s, %s, %s, %s)""",
                (emp_id, course_id, class_id, status))

    # commit the command
    conn.commit()

    # close sql connection
    cur.close()

    return("Successfully Pending Enroll"), 201

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
