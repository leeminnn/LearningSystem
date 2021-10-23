import requests
import datetime
from flask import jsonify, Flask, request
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
import time
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

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

    if not request.json:
        return("Invalid body request."), 400

    course_id = request.json['course_id']
    course_name = request.json['course_name']
    course_desc = request.json ['course_desc']
    pre_req = request.json['pre_req']

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""INSERT INTO course.course(course_id, course_name, course_desc, pre_req) VALUES (%s, %s, %s, %s)""",
                (course_id, course_name, course_desc, pre_req))

    conn.commit()
    cur.close()

    return("Successfully Create Course"), 200

#HR Create new class to assign trainers after creating a new course
@app.route('/create_class', methods=['POST']) 
def create_class():
    #check for body request
    if not request.json:
        return("Invalid body request."), 400
    
    class_id = request.json['class_id'];
    intake = request.json['intake'];
    emp_id = request.json['emp_id'];
    emp_name = request.json['emp_name'];
    course_id = request.json['course_id'];
    course_name = request.json['course_name'];
    start_date = request.json['start_date'];
    end_date = request.json['end_date'];
    start_enrol = request.json['start_enrol'];
    end_enrol = request.json['end_enrol'];

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""INSERT INTO course.class(class_id,intake,emp_id, emp_name, course_id, course_name, start_date, end_date, start_enrol, end_enrol)
     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (class_id,intake,emp_id, emp_name, course_id, course_name, start_date, end_date, start_enrol, end_enrol))   
    
    conn.commit()
    cur.close()

    return("Successfully Create Class"), 200
    
#HR update course
@app.route('/update_course', methods=['PUT']) 
def update_class():
    #check for body request
    if not request.json:
        return ("Invalid body request."),400

    course_id = request.json['course_id']
    course_name = request.json['course_name']
    course_desc = request.json ['course_desc']
    pre_req = request.json['pre_req']

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""UPDATE course.course SET course_name = %s, course_desc = %s, pre_req=%s
                WHERE course_id = %s """,
                (course_name, course_desc, pre_req, course_id))

    conn.commit()
    cur.close()

    return("Successfully Update Course"), 200

#get all courses
@app.route("/all_courses", methods=['POST']) 
def all_courses():

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM course.course")

    result = cur.fetchall()
    return jsonify(result), 200

## learner want to enroll to the course / hr wants to enrol learner##
@app.route('/enrol', methods=['POST']) 
def enrol():

    if not request.json:
        return("Invalid body request."), 400

    emp_id = request.json['emp_id']
    emp_name = request.json['emp_name']
    course_id = request.json['course_id']
    course_name = request.json['course_name']
    class_id = request.json['class_id']
    pending_status = request.json['pending_status']

    conn = mysql.connect()
    cur = conn.cursor()

    cur.execute("""INSERT INTO course.pending_enrolment(emp_id, emp_name, course_id, course_name, class_id, pending_status) VALUES (%s, %s, %s, %s, %s, %s)""",

                (emp_id, emp_name, course_id, course_name, class_id, pending_status))

    conn.commit()
    cur.close()

    return("Successfully Pending Enroll"), 200

# delete course
@app.route('/remove', methods=['DELETE'])
def remove_course():

    if not request.json:
        return("Invalid body request."), 400

    course_id = request.json['course_id']

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM course.course WHERE course_id=%s", (course_id))

    conn.commit()
    cur.close()

    return("Successfully delete course"), 200

#approve learner enrolment
@app.route('/approve_learner', methods=['PUT'])
def approve_learner():

    if not request.json:
        return("Invalid body request."), 400

    pending_status = 'approve'
    emp_id = request.json['emp_id']
    class_id = request.json['class_id']
    course_id = request.json['course_id']

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""UPDATE course.pending_enrolment SET pending_status = %s
                WHERE emp_id = %s AND class_id = %s AND course_id=%s""",
                (pending_status, emp_id,class_id,course_id))

    conn.commit()
    cur.close()

    return("Successfully update learner's pending enrolment status"), 200
  
#as a learner & trainer, able to view course progress 
@app.route("/learner_progress", methods=['POST'])
def learner_progress():
    
    if not request.json:
        return("Invalid body request."), 400

    emp = request.json['emp_id']

    conn = mysql.connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM course.class_list WHERE emp_id=%s", (emp))

    result = cur.fetchall()
    return jsonify(result), 200

#as a learner, view course outline and description
@app.route("/course_info", methods=['POST'])
def course_info():
        # check for body request
    if not request.json:
        return("Invalid body request."), 400

    course_id = request.json['course_id']

    conn = mysql.connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM course.course WHERE course_id=%s", (course_id))

    result = cur.fetchall()
    return jsonify(result), 200


# get eligible courses - compare pre-req 
@app.route("/get_learner_eligible_courses/<string:course_id>", methods=['GET'])
def eligible_courses(course_id):

    conn = mysql.connect()
    cur = conn.cursor()
    course_id = course_id.strip('][').split(',')
    if course_id == []:
        cur.execute("""SELECT * FROM course.course WHERE pre_req IS NULL""")
    else:
        print(tuple(course_id))
        cur.execute("""SELECT * FROM course.course WHERE pre_req IN %s OR pre_req IS NULL""" ,[tuple(course_id)])

    result = cur.fetchall()
    return jsonify(result), 200

#as a learner, get in progress
@app.route("/get_inprogress_course/<string:course_id>", methods=['GET'])
def get_inprogress_course(course_id):
    conn = mysql.connect()
    cur = conn.cursor()
    course_id = course_id.strip('][').split(',')
    print(tuple(course_id))
    cur.execute("""SELECT * FROM course.course WHERE course_id IN %s""" ,[tuple(course_id)])


    result = cur.fetchall()
    return jsonify(result), 200

#as a learner, learner completed courses 
@app.route("/completed_courses/<string:course_id>", methods=['GET'])
def completed_courses(course_id):
    conn = mysql.connect()
    cur = conn.cursor()
    course_id = course_id.strip('][').split(',')
    cur.execute("""SELECT * FROM course.course WHERE course_id IN %s""",[tuple(course_id)])

    result = cur.fetchall()
    return jsonify(result), 200

#as a trainer, get ongoing courses
@app.route("/get_trainer_ongoing_courses/<string:course_id>", methods=['GET'])
def get_trainer_ongoing_courses(course_id):
    conn = mysql.connect()
    cur = conn.cursor()
    course_id = course_id.strip('][').split(',')
    cur.execute("""SELECT * FROM course.course WHERE course_id IN %s""" ,[tuple(course_id)])

    result = cur.fetchall()
    return jsonify(result), 200

#as a trainer, get completed courses
@app.route("/get_trainer_completed_courses/<string:course_id>", methods=['GET'])
def get_trainer_completed_courses(course_id):
    conn = mysql.connect()
    cur = conn.cursor()
    course_id = course_id.strip('][').split(',')
    cur.execute("""SELECT * FROM course.course WHERE course_id IN %s""" ,[tuple(course_id)])

    result = cur.fetchall()
    return jsonify(result), 200

# Get list of pending approval based on course id and class id
@app.route("/pending_approval", methods=['POST'])
def pending_approval():
        # check for body request
    if not request.json:
        return("Invalid body request."), 400

    course_id = request.json['course_id']
    class_id = request.json['class_id']

    conn = mysql.connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM course.pending_enrolment WHERE course_id=%s AND class_id =%s AND pending_status='Pending'", (course_id, class_id))

    result = cur.fetchall()
    return jsonify(result), 200

# Get list of course_id of ineligible courses -- KIV
@app.route("/ineligible_courses", methods=['POST'])
def ineligible_courses():
        # check for body request
    if not request.json:
        return("Invalid body request."), 400

    course_id = request.json['course_id']

    conn = mysql.connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM course.course WHERE course_id=%s", (course_id))

    result = cur.fetchall()
    return jsonify(result), 200

#Learner to view selected classes during certain period 
@app.route('/selected_date', methods=['POST'])
def selected_date():

    date = time.strftime("%Y-%m-%d")
    conn = mysql.connect()
    cur = conn.cursor()

    cur.execute("""SELECT * FROM course.class WHERE %s BETWEEN start_date AND end_date""", [date])
    
    result = cur.fetchall()
    return jsonify(result), 200

#update learner's or trainer's class_list status to withdraw or completed: 
@app.route('/update_status', methods=['PUT'])
def update_status():

    if not request.json:
        return ("Invalid body request."),400

    class_status = request.json['class_status']
    emp_id = request.json['emp_id']
    
    class_id = request.json['class_id']

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""UPDATE course.class_list SET class_status = %s
                WHERE emp_id = %s AND class_id = %s """,(class_status, emp_id, class_id))
    
    conn.commit()
    cur.close()

    return("Successfully update learner's or trainer's class_list status"), 200

#List of classes based on courses id
@app.route("/available_classes", methods=['POST'])
def available_classes():
        # check for body request
    if not request.json:
        return("Invalid body request."), 400

    course_id = request.json['course_id']

    conn = mysql.connect()
    cur = conn.cursor()

    cur.execute("SELECT class_id FROM course.class WHERE course_id=%s",(course_id))

    result = cur.fetchall()
    return jsonify(result), 200

#get courses name and id for pre-req dropdown to create course
@app.route("/prereq_dropdown", methods=['GET'])
def prereq_dropdown():

    conn = mysql.connect()
    cur = conn.cursor()

    cur.execute("SELECT course_id, course_name FROM course.course")

    result = cur.fetchall()
    return jsonify(result), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

