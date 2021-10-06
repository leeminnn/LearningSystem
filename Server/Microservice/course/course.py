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


## learner want to enroll to the course ##
#as a learner, want to enroll to the course that I am interested..
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
    cur.execute("INSERT INTO course.pending_enrolment(emp_id, course_id, class_id, status) VALUES (%s, %s, %s, %s)",
                (emp_id, course_id, class_id, status))

    # commit the command
    conn.commit()

    # close sql connection
    cur.close()

    return("Success"), 201


@app.route("/all_courses", methods=['GET'])
def all_courses():

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM COURSE")
    result = cur.fetchall()

    return jsonify(result), 203


@app.route('/add_course', methods=['POST'])
def add_course():

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
    cur.execute("INSERT INTO COURSE(course_id, course_name, start_date,end_date,pre_requisite) VALUES (%s, %s, %s, %s, %s)",
                (course_id, course_name, start_date, end_date, pre_requisite))

    # commit the command
    conn.commit()

    # close sql connection
    cur.close()

    return("Success"), 201


@app.route('/remove', methods=['DELETE'])
def remove_course():

    if not request.json:
        return("Invalid body request."), 400

    course_id = request.json['course_id']

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM COURSE WHERE course_id=%s", [course_id])
    conn.commit()
    cur.close()

    return("Success"), 202


#as a leaner & trainer, able to view course progress 
@app.route("/leaner_progress", methods=['GET'])
def learner_progresss():

    emp = request.json['emp_id']
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""SELECT * FROM course.learner_list WHERE emp_id=%s""", [emp])
    result = cur.fetchall()

    return jsonify(result), 204


#as a leaner, view course outline and description 
#as leaner, view course materials
@app.route("/course_info", methods=['GET'])
def course_info():

    course_id = request.json['course_id']
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""SELECT * FROM course WHERE course_id=%s""", [course_id])
    result = cur.fetchall()

    return jsonify(result), 205


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
