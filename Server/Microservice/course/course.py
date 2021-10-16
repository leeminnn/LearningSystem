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

    return("Success"), 202

#Learner to view selected course during certain period 
@app.route("/view_available_course/<string:date>", methods=['GET'])
def get_one():
                # check for body request
    if not request.json:
        return("Invalid body request."), 400

    date = request.json["date"]
    
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""SELECT * FROM course.course WHERE %s BETWEEN start_date AND end_date""", [date])
    result = cur.fetchall()
    conn.commit()
    cur.close()


    return jsonify(result), 203

#update learner's or trainer's class_list status to withdraw or completed: 
@app.route('/update_status', methods=['PUT'])
def update_status():

    if not request.json:
        return ("Invalid body request."),400

    status = request.json['status']
    emp_id = request.json['emp_id']
    course_id = request.json['course_id']
    class_id = request.json['class_id']

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""UPDATE course.class_list SET status = %s, course_id = %s, class_id = %s
                WHERE emp_id = %s """,(status, emp_id, course_id, class_id))
    
    result = cur.fetchall()
    conn.commit()
    cur.close()

    return jsonify(result), 203

#approve learner enrolment
@app.route('/approve_learner', methods=['PUT'])
def approve_learner():

    if not request.json:
        return("Invalid body request."), 400

    status = request.json['status']
    emp_id = request.json['emp_id']

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""UPDATE course.pending_enrolment SET status = %s
                WHERE emp_id = %s """,
                (status, emp_id))
    conn.commit()
    cur.close()
    return("Success"), 202
  
#as a learner & trainer, able to view course progress 
@app.route("/learner_progress", methods=['GET'])
def learner_progresss():
    
    if not request.json:
        return("Invalid body request."), 400

    emp = request.json['emp_id']

    conn = mysql.connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM course.class_list WHERE emp_id=%s", (emp))

    result = cur.fetchall()

    return jsonify(result), 203


#as a learner, view course outline and description
@app.route("/course_info", methods=['GET'])
def course_info():
        # check for body request
    if not request.json:
        return("Invalid body request."), 400

    course_id = request.json['course_id']

    conn = mysql.connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM course.course WHERE course_id=%s", (course_id))

    result = cur.fetchall()

    return jsonify(result), 203


# get eligible courses - compare pre-req 
@app.route("/eligible_courses", methods=['GET'])
def eligible_courses():
        # check for body request
    if not request.json:
        return("Invalid body request."), 400

    course_id = request.json['course_id']

    conn = mysql.connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM course.course WHERE course_id=%s", (course_id))

    result = cur.fetchall()

    return jsonify(result), 203


# Get list of pending approval based on course id and class id
@app.route("/pending_approval", methods=['GET'])
def pending_approval():
        # check for body request
    if not request.json:
        return("Invalid body request."), 400

    course_id = request.json['course_id']
    class_id = request.json['class_id']

    conn = mysql.connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM course.pending_enrolment WHERE course_id=%s, class_id =%s", (course_id, class_id))

    result = cur.fetchall()

    return jsonify(result), 203



# Get list of course_id of ineligible courses
@app.route("/ineligible_courses", methods=['GET'])
def ineligible_courses():
        # check for body request
    if not request.json:
        return("Invalid body request."), 400

    course_id = request.json['course_id']

    conn = mysql.connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM course.course WHERE course_id=%s", (course_id))

    result = cur.fetchall()

    return jsonify(result), 203



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

