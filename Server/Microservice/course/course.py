import requests
from datetime import datetime
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


# HR create new course
@app.route('/create_course', methods=['POST'])
def create_course():

    if not request.json:
        return("Invalid body request."), 400

    course_id = request.json['course_id']
    course_name = request.json['course_name']
    course_desc = request.json['course_desc']
    pre_req = request.json['pre_req']

    if pre_req == "":
        pre_req = "No Prerequisite Course"

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""INSERT INTO course.course(course_id, course_name, course_desc, pre_req) VALUES (%s, %s, %s, %s)""",
                (course_id, course_name, course_desc, pre_req))

    conn.commit()
    cur.close()

    return("Successfully Create Course"), 200

# HR Create new class to assign trainers after creating a new course


@app.route('/create_class', methods=['POST'])
def create_class():
    # check for body request
    if not request.json:
        return("Invalid body request."), 400

    intake = request.json['intake']
    emp_id = request.json['emp_id']
    emp_name = request.json['emp_name']
    course_id = request.json['course_id']
    start_date = request.json['start_date']
    end_date = request.json['end_date']
    start_enrol = request.json['start_enrol']
    end_enrol = request.json['end_enrol']

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""INSERT INTO course.class(intake,emp_id, emp_name, course_id, start_date, end_date, start_enrol, end_enrol)
     VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                (intake, emp_id, emp_name, course_id, start_date, end_date, start_enrol, end_enrol))
    conn.commit()
    cur.execute("""SELECT class_id FROM course.class
        WHERE intake=%s and emp_id=%s and emp_name=%s and course_id=%s and start_date=%s and end_date=%s and start_enrol=%s and end_enrol=%s""",
                (intake, emp_id, emp_name, course_id, start_date, end_date, start_enrol, end_enrol))
    result = cur.fetchall()
    class_id = result[0]['class_id']
    conn.commit()
    cur.execute("""INSERT INTO course.class_list(emp_id, emp_name, class_id, class_status) VALUES (%s, %s, %s, %s)""",
                (emp_id, emp_name, class_id, 'trainer'))
    conn.commit()

    cur.execute("""UPDATE employee.trainer SET courses_teaching = concat(courses_teaching, ',' , %s)
                WHERE emp_id = %s """,
                (course_id, emp_id))

    conn.commit()

    cur.execute("""INSERT INTO section.section(section_id, class_id, course_id) VALUES (%s, %s, %s)""",
                (1, class_id, course_id))
    conn.commit()
    cur.execute("""INSERT INTO section.quiz(section_id, class_id, course_id, quiz_type) VALUES (%s, %s, %s, %s)""",
                (1, class_id, course_id, 'ungraded'))
    conn.commit()
    cur.close()

    return("Successfully Create Class"), 200

# HR update course


@app.route('/update_course', methods=['PUT'])
def update_class():
    # check for body request
    if not request.json:
        return ("Invalid body request."), 400

    course_id = request.json['course_id']
    course_name = request.json['course_name']
    course_desc = request.json['course_desc']
    pre_req = request.json['pre_req']

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""UPDATE course.course SET course_name = %s, course_desc = %s, pre_req=%s
                WHERE course_id = %s """,
                (course_name, course_desc, pre_req, course_id))

    conn.commit()
    cur.close()

    return("Successfully Update Course"), 200

# get all courses


@app.route("/all_courses", methods=['GET', 'POST'])
def all_courses():

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM course.course WHERE active='active'")

    result = cur.fetchall()
    for i in result:
        i['course_id'] = str(i['course_id']).rjust(3, '0')
        if i['pre_req'] != "No Prerequisite Course":
            cur.execute(
                """SELECT course_name FROM course.course WHERE course_id=%s """, (i['pre_req']))
            res = cur.fetchall()
            i['pre_req'] = res[0]['course_name']

    conn.commit()
    cur.close()

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
    pending_status = "pending"

    conn = mysql.connect()
    cur = conn.cursor()

    cur.execute("""INSERT INTO course.pending_enrolment(emp_id, emp_name, course_id, course_name, class_id, pending_status) VALUES (%s, %s, %s, %s, %s, %s)""",
                (emp_id, emp_name, course_id, course_name, class_id, pending_status))

    conn.commit()
    cur.close()

    return("Successfully Pending Enroll"), 200


@app.route('/assign_engineer', methods=['POST', 'PUT'])
def assign_engineer():

    if not request.json:
        return("Invalid body request."), 400

    learner = request.json['learner']
    class_id = request.json['class_id']
    course_id = request.json['course_id']
    learner_name = request.json['learnerName']

    conn = mysql.connect()
    cur = conn.cursor()
    for i in range(len(learner)):
        emp_name = learner_name[i]
        emp_id = learner[i]
        cur.execute("""INSERT INTO course.class_list(emp_id, emp_name, class_id, class_status) VALUES (%s, %s, %s, %s)""",
                    (emp_id, emp_name, class_id, 'learner'))
        conn.commit()
        cur.execute("""UPDATE employee.learner SET courses_ongoing = concat(courses_ongoing, ',' , %s)
            WHERE emp_id = %s """,
                    (course_id, emp_id))
        conn.commit()

    cur.close()

    return("Success"), 200

# delete course


@app.route('/remove', methods=['PUT'])
def remove_course():

    if not request.json:
        return("Invalid body request."), 400

    course_id = request.json['course_id']

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute(
        """UPDATE course.course SET active = 'inactive' WHERE course_id=%s""", (course_id))
    conn.commit()
    cur.close()

    return("Successfully delete course"), 200

# approve learner enrolment


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
                (pending_status, emp_id, class_id, course_id))

    conn.commit()
    cur.close()

    return("Successfully update learner's pending enrolment status"), 200

# as a learner & trainer, able to view course progress


@app.route("/learner_progress", methods=['POST'])
def learner_progress():

    if not request.json:
        return("Invalid body request."), 400

    emp = request.json['emp_id']
    class_id = request.json['class_id']

    conn = mysql.connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM course.class_list WHERE emp_id=%s and class_id=%s", (emp, class_id))

    result = cur.fetchall()
    conn.commit()
    cur.close()
    return jsonify(result[0]), 200

# as a learner, view course outline and description


@ app.route("/course_info", methods=['POST'])
def course_info():
    # check for body request
    if not request.json:
        return("Invalid body request."), 400

    course_id = request.json['course_id']

    conn = mysql.connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM course.course WHERE course_id=%s", (course_id))

    result = cur.fetchall()

    conn.commit()
    cur.close()
    return jsonify(result), 200


# get eligible courses - compare pre-req
@ app.route("/eligible", methods=['POST'])
def eligible():

    if not request.json:
        return("Invalid body request."), 400

    emp_id = request.json['emp_id']
    final = []
    onGoing = []

    conn = mysql.connect()
    cur = conn.cursor()

    cur.execute(
        """SELECT courses_completed FROM employee.learner WHERE emp_id=%s""", (emp_id))
    result = cur.fetchall()
    conn.commit()
    course_completed = result[0]['courses_completed'].split(',')

    cur.execute(
        """SELECT courses_ongoing FROM employee.learner WHERE emp_id=%s""", (emp_id))
    result = cur.fetchall()
    conn.commit()
    courses_ongoing = result[0]['courses_ongoing'].split(',')
    for i in courses_ongoing:
        if i != '' and int(i) not in onGoing:
            onGoing.append(int(i))
        elif i == '':
            onGoing.append(i)

    for i in course_completed:
        if i == '':
            cur.execute(
                """SELECT * FROM course.course WHERE pre_req='No Prerequisite Course' and active='active'""")
        else:
            cur.execute(
                """SELECT * FROM course.course WHERE pre_req=%s and active='active'""", (i))
        result = cur.fetchall()
        conn.commit()
        for i in result:
            if i['course_id'] not in onGoing:
                i['course_id'] = str(i['course_id']).rjust(3, '0')
                final.append(i)

    cur.close()
    return jsonify(final), 200

# as a learner, get in progress


@ app.route("/in_progress", methods=['POST'])
def in_progress():

    if not request.json:
        return("Invalid body request."), 400

    emp_id = request.json['emp_id']
    final = []
    onGoing = []

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute(
        """SELECT courses_ongoing FROM employee.learner WHERE emp_id=%s""", (emp_id))
    result = cur.fetchall()
    conn.commit()
    courses_ongoing = result[0]['courses_ongoing'].split(',')
    for i in courses_ongoing:
        if i != '' and int(i) not in onGoing:
            onGoing.append(int(i))
        elif i == '':
            onGoing.append(i)

    for o in onGoing:
        if o != "":
            cur.execute(
                """SELECT * FROM course.course WHERE course_id=%s """, (o))
            conn.commit()
            result = cur.fetchall()
            for i in result:
                i['course_id'] = str(i['course_id']).rjust(3, '0')
                if i['pre_req'] != "No Prerequisite Course":
                    cur.execute(
                        """SELECT course_name FROM course.course WHERE course_id=%s""", (i['pre_req']))
                    res = cur.fetchall()
                    i['pre_req'] = res[0]['course_name']
                final.append(i)

    cur.close()
    return jsonify(final), 200

# as a learner, learner completed courses


@ app.route("/completed", methods=['POST'])
def completed():

    if not request.json:
        return("Invalid body request."), 400

    emp_id = request.json['emp_id']
    final = []
    completed = []

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute(
        """SELECT courses_completed FROM employee.learner WHERE emp_id=%s""", (emp_id))
    result = cur.fetchall()
    conn.commit()
    courses_completed = result[0]['courses_completed'].split(',')
    for i in courses_completed:
        if i != '' and int(i) not in completed:
            completed.append(int(i))
        elif i == '':
            completed.append(i)

    for o in completed:
        if o != "":
            cur.execute(
                """SELECT * FROM course.course WHERE course_id=%s""", (o))
            conn.commit()
            result = cur.fetchall()
            final.append(result[0])

    cur.close()
    return jsonify(final), 200

# as a trainer, get ongoing courses


@ app.route("/get_trainer_ongoing_courses", methods=['POST'])
def get_trainer_ongoing_courses():

    if not request.json:
        return("Invalid body request."), 400

    emp_id = request.json['emp_id']
    final = []

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute(
        """SELECT courses_teaching FROM employee.trainer WHERE emp_id=%s""", (emp_id))
    result = cur.fetchall()
    conn.commit()
    course_teaching = result[0]['courses_teaching'].split(',')
    for course_id in course_teaching:
        if course_id != '':
            cur.execute(
                """SELECT * FROM course.course WHERE course_id=%s""", (course_id))
            result = cur.fetchall()
            conn.commit()
            final.append(result[0])
    cur.close()
    return jsonify(final), 200

# as a trainer, get completed courses


@ app.route("/get_trainer_completed_courses", methods=['POST'])
def get_trainer_completed_courses():

    if not request.json:
        return("Invalid body request."), 400

    emp_id = request.json['emp_id']
    final = []

    conn = mysql.connect()
    cur = conn.cursor()

    cur.execute(
        """SELECT courses_completed FROM employee.trainer WHERE emp_id=%s""", (emp_id))
    result = cur.fetchall()
    conn.commit()
    course_teaching = result[0]['courses_completed'].split(',')
    for course_id in course_teaching:
        if course_id != '':
            cur.execute(
                """SELECT * FROM course.course WHERE course_id=%s""", (course_id))
            result = cur.fetchall()
            conn.commit()
            final.append(result[0])
    cur.close()
    return jsonify(final), 200

# Get list of pending approval based on course id and class id


@ app.route("/pending_approval", methods=['POST'])
def pending_approval():
    # check for body request
    if not request.json:
        return("Invalid body request."), 400

    course_id = request.json['course_id']
    class_id = request.json['class_id']

    conn = mysql.connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM course.pending_enrolment WHERE course_id=%s AND class_id =%s AND pending_status='pending'", (course_id, class_id))

    result = cur.fetchall()
    conn.commit()
    cur.close()
    return jsonify(result), 200

# Get list of course_id of ineligible courses -- KIV


@ app.route("/ineligible_courses", methods=['POST'])
def ineligible_courses():
    # check for body request
    if not request.json:
        return("Invalid body request."), 400

    course_id = request.json['course_id']

    conn = mysql.connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM course.course WHERE course_id=%s", (course_id))

    result = cur.fetchall()
    conn.commit()
    cur.close()
    return jsonify(result), 200

# Learner to view selected classes during certain period


@ app.route('/selected_date', methods=['POST'])
def selected_date():

    date = time.strftime("%Y-%m-%d")
    conn = mysql.connect()
    cur = conn.cursor()

    cur.execute(
        """SELECT * FROM course.class WHERE %s BETWEEN start_date AND end_date""", [date])

    result = cur.fetchall()
    conn.commit()
    cur.close()
    return jsonify(result), 200

# update learner's or trainer's class_list status to withdraw or completed:


@ app.route('/update_status', methods=['PUT'])
def update_status():

    if not request.json:
        return ("Invalid body request."), 400

    class_status = request.json['class_status']
    emp_id = request.json['emp_id']

    class_id = request.json['class_id']

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""UPDATE course.class_list SET class_status = %s
                WHERE emp_id = %s AND class_id = %s """, (class_status, emp_id, class_id))

    conn.commit()
    cur.close()

    return("Successfully update learner's or trainer's class_list status"), 200

# List of classes based on courses id


@ app.route("/available_classes", methods=['POST'])
def available_classes():
    # check for body request
    if not request.json:
        return("Invalid body request."), 400

    course_id = request.json['course_id']

    conn = mysql.connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT class_id FROM course.class WHERE course_id=%s", (course_id))

    result = cur.fetchall()
    conn.commit()
    cur.close()
    return jsonify(result), 200

# get courses name and id for pre-req dropdown to create course


@ app.route("/prereq_dropdown", methods=['GET'])
def prereq_dropdown():

    conn = mysql.connect()
    cur = conn.cursor()

    cur.execute("SELECT course_id, course_name FROM course.course")

    result = cur.fetchall()
    conn.commit()
    cur.close()
    return jsonify(result), 200


@ app.route("/all_classes", methods=['POST'])
def all_classes():
    # check for body request
    if not request.json:
        return("Invalid body request."), 400

    course_id = request.json['course_id']

    conn = mysql.connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM course.class WHERE course_id=%s", (course_id))
    result = cur.fetchall()

    conn.commit()
    cur.close()

    return jsonify(result), 200


@ app.route("/get_classes", methods=['POST'])
def get_classes():
    # check for body request
    if not request.json:
        return("Invalid body request."), 400

    course_id = request.json['course_id']
    emp_id = request.json['emp_id']

    conn = mysql.connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM course.class WHERE course_id=%s and emp_id=%s", (course_id, emp_id))
    result = cur.fetchall()

    conn.commit()
    cur.close()

    return jsonify(result), 200


@ app.route("/get_learner_classes", methods=['POST'])
def get_learner_classes():
    # check for body request
    if not request.json:
        return("Invalid body request."), 400

    course_id = request.json['course_id']
    emp_id = request.json['emp_id']
    final = []

    conn = mysql.connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT class_id FROM course.class_list WHERE emp_id=%s", (emp_id))
    result = cur.fetchall()
    for i in result:
        cur.execute(
            "SELECT * FROM course.class WHERE course_id=%s and class_id=%s", (course_id, i['class_id']))
        res = cur.fetchall()
        if len(res) != 0:
            final.append(res[0])

    conn.commit()
    cur.close()

    return jsonify(final), 200


@ app.route('/add_course', methods=['POST'])
def add_course():

    # check for body request
    if not request.json:
        return("Invalid body request."), 400

    course_name = request.json['course_name']
    course_desc = request.json['course_desc']
    pre_req = request.json['pre_req']
    if pre_req == '':
        pre_req = "No Prerequisite Course"

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO course.course(course_name,course_desc, pre_req) VALUES (%s, %s, %s)",
                (course_name, course_desc, pre_req))

    # commit the command
    conn.commit()
    # close sql connection
    cur.close()

    return("Success"), 200


@ app.route("/get_class_list", methods=['POST'])
def get_class_list():

    if not request.json:
        return("Invalid body request."), 400

    class_id = request.json['class_id']

    conn = mysql.connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM course.class_list WHERE class_id=%s;", (class_id))
    result = cur.fetchall()

    conn.commit()
    cur.close()

    return jsonify(result), 200


@ app.route("/withdraw_learners", methods=['DELETE'])
def withdraw_learners():

    final = []
    string = ''
    class_id = request.json['class_id']
    course_id = request.json['course_id']

    if not request.json:
        return("Invalid body request."), 400
    conn = mysql.connect()
    cur = conn.cursor()

    learners_array = request.json['learner']
    for i in learners_array:
        emp_id = i['empid']
        cur.execute(
            "DELETE FROM course.class_list WHERE emp_id=%s and class_id=%s;", (emp_id, class_id))
        result = cur.fetchall()
        conn.commit()
        final.append(result)
        cur.execute(
            """SELECT courses_ongoing FROM employee.learner where emp_id=%s""", (emp_id))
        res = cur.fetchall()
        conn.commit()
        courses_ongoing = res[0]['courses_ongoing'].split(',')
        for c in courses_ongoing:
            if c != course_id:
                string += ',' + c
        cur.execute(
            """UPDATE employee.learner SET courses_ongoing = %s WHERE emp_id = %s """, (string, emp_id))
        conn.commit()

    conn.commit()
    cur.close()

    return jsonify(result), 200


@ app.route("/all_eligible_classes", methods=['POST'])
def all_eligible_classes():
    # check for body request
    if not request.json:
        return("Invalid body request."), 400

    course_id = request.json['course_id']
    today = datetime.now()
    dt_string = today.strftime("%d/%m/%Y")
    final = []

    conn = mysql.connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM course.class WHERE course_id=%s", (course_id))
    result = cur.fetchall()
    for i in result:
        if datetime.strftime(i['start_date'], "%Y/%m/%d") < dt_string and datetime(i['end_date'],  "%Y/%m/%d") > dt_string:
            final.append(i)

    conn.commit()
    cur.close()

    return jsonify(final), 200


@app.route('/enroll_engineer', methods=['PUT'])
def enroll_engineer():

    if not request.json:
        return("Invalid body request."), 400

    learner = request.json['learner']
    class_id = request.json['class_id']
    course_id = request.json['course_id']
    learner_name = request.json['learnerName']

    conn = mysql.connect()
    cur = conn.cursor()
    for i in range(len(learner)):
        emp_name = learner_name[i]
        emp_id = learner[i]
        cur.execute(
            "UPDATE course.pending_enrolment SET pending_status = 'Approval' WHERE emp_id =%s and class_id =%s;", (emp_id, class_id))
        cur.execute("""INSERT INTO course.class_list(emp_id, emp_name, class_id, class_status) VALUES (%s, %s, %s, %s)""",
                    (emp_id, emp_name, class_id, 'learner'))

    conn.commit()
    cur.close()

    return("Success"), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
