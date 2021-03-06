from datetime import datetime
from flask import jsonify, Flask, request
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
from flask_cors import CORS
import os

app = Flask(__name__)
cors = CORS(app)

app.config['MYSQL_DATABASE_HOST'] = os.environ['dbURL']
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'course'

mysql = MySQL(app, cursorclass=DictCursor)
mysql.init_app(app)


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

    quiz_id = str(course_id) + str(class_id)
    quiz_id = int(quiz_id)
    cur.execute("""INSERT INTO section.quiz(quiz_id, class_id, course_id, total_mark, quiz_type, time) VALUES ( %s, %s, %s, %s, %s, %s)""",
                (quiz_id, class_id, course_id, 50, 'graded', 4200))
    conn.commit()
    cur.execute(
        """SELECT MAX(quiz_id) FROM section.quiz WHERE quiz_type='ungraded'""")
    result = cur.fetchall()
    conn.commit()
    print(result)
    if result[0]['MAX(quiz_id)'] == None:
        quiz_id = 1

    else:
        quiz_id = result[0]['MAX(quiz_id)'] + 1
    cur.execute("""INSERT INTO section.quiz(quiz_id, section_id, class_id, course_id, total_mark, quiz_type) VALUES (%s, %s, %s, %s, %s, %s)""",
                (quiz_id, 1, class_id, course_id, 0, 'ungraded'))
    conn.commit()

    quiz_id += 1
    # ALTER TABLE course.course AUTO_INCREMENT=100;
    cur.execute("""ALTER TABLE section.quiz AUTO_INCREMENT=%s""",
                (quiz_id))
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
    cur.execute("SELECT * FROM course.course WHERE course_active='active'")

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
    class_id = request.json['class_id']
    pending_status = "pending"

    conn = mysql.connect()
    cur = conn.cursor()

    cur.execute("""INSERT INTO course.pending_enrolment(emp_id, emp_name, course_id, class_id, pending_status) VALUES (%s, %s, %s, %s, %s)""",
                (emp_id, emp_name, course_id, class_id, pending_status))

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
        """UPDATE course.course SET course_active = 'inactive' WHERE course_id=%s""", (course_id))
    conn.commit()
    cur.execute(
        """ALTER TABLE course.course AUTO_INCREMENT=1""")
    conn.commit()
    cur.close()

    return("Successfully delete course"), 200


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
    pending = []
    enrolled = []

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

    cur.execute(
        """SELECT * FROM course.pending_enrolment WHERE emp_id=%s and pending_status='pending'""", (emp_id))
    res = cur.fetchall()
    for i in res:
        pending.append(i['course_id'])
    conn.commit()

    for i in pending:
        cur.execute(
            """SELECT * FROM course.course WHERE course_id=%s and course_active='active'""", (i))
        r = cur.fetchall()
        r[0]['course_id'] = str(r[0]['course_id']).rjust(3, '0')
        enrolled.append(r[0])
        conn.commit()

    for i in course_completed:
        if i == '':
            cur.execute(
                """SELECT * FROM course.course WHERE pre_req='No Prerequisite Course' and course_active='active'""")
        else:
            cur.execute(
                """SELECT * FROM course.course WHERE pre_req=%s and course_active='active'""", (i))
        result = cur.fetchall()
        conn.commit()
    for i in result:
        if i['course_id'] not in onGoing:
            if i['course_id'] not in pending:
                i['course_id'] = str(i['course_id']).rjust(3, '0')
                final.append(i)

    cur.close()
    return jsonify({'eligible': final, 'Pending': enrolled}), 200

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
    for i in result:
        if i['graded_result'] == "pass":
            i['status'] = 'Completed'
        elif i['graded_result'] == None:
            i['status'] = "In Progress"
        else:
            i['status'] = "Incomplete"

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
        print(i)
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
    dt_string = datetime.now().date()
    print(dt_string)
    final = []

    conn = mysql.connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM course.class WHERE course_id=%s", (course_id))
    result = cur.fetchall()
    for i in result:
        if i['start_enrol'] < dt_string and i['end_enrol'] > dt_string:
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
        conn.commit()
        cur.execute("""INSERT INTO course.class_list(emp_id, emp_name, class_id, class_status) VALUES (%s, %s, %s, %s)""",
                    (emp_id, emp_name, class_id, 'learner'))
        conn.commit()
        cur.execute("""UPDATE employee.learner SET courses_ongoing = concat(courses_ongoing, ',' , %s)
            WHERE emp_id = %s """,
                    (course_id, emp_id))

        conn.commit()

    cur.close()

    return("Success"), 200


@app.route('/pass_final_quiz', methods=['PUT'])
def pass_final_quiz():
    if not request.json:
        return("Invalid body request."), 400
    conn = mysql.connect()
    cur = conn.cursor()

    class_id = request.json['class_id']
    emp_id = request.json['emp_id']
    result = request.json['result']
    course_id = request.json['course_id']
    course_id = str(request.json['course_id']).rjust(3, '0')

    cur.execute("""UPDATE course.class_list set graded_result=%s WHERE emp_id=%s AND class_id=%s""",
                (result, emp_id, class_id))
    conn.commit()

    if result == 'pass':
        cur.execute(
            """SELECT courses_ongoing FROM employee.learner WHERE emp_id=%s""", (emp_id))
        result = cur.fetchall()
        conn.commit()
        ongoing = result[0]['courses_ongoing'].split(',')
        string = ''
        for i in ongoing:
            if i != course_id:
                string += ',' + i
        string = string.strip(',')
        cur.execute("""UPDATE employee.learner SET courses_ongoing = %s
            WHERE emp_id = %s """,
                    (string, emp_id))
        conn.commit()

        cur.execute("""UPDATE employee.learner SET courses_completed = concat(courses_completed, ',' , %s)
            WHERE emp_id = %s """,
                    (course_id, emp_id))
        conn.commit()

    cur.close()

    return("Success"), 200


@ app.route("/remove_pending", methods=['DELETE'])
def remove_pending():
    # check for body request
    if not request.json:
        return("Invalid body request."), 400

    course_id = request.json['course_id']
    learner = request.json['learner']

    conn = mysql.connect()
    cur = conn.cursor()

    for i in range(len(learner)):
        emp_id = learner[i]
        cur.execute(
            """DELETE FROM course.pending_enrolment WHERE emp_id=%s and course_id=%s""", (emp_id, course_id))
        conn.commit()

    cur.close()
    return("Success"), 200


@ app.route("/ended_classes", methods=['GET'])
def ended_classes():

    dt_string = datetime.now().date()
    #dt_string = today.strftime("%d/%m/%Y")
    print(dt_string)

    conn = mysql.connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT course_id,class_id FROM course.class WHERE end_date < %s", (dt_string))
    result = cur.fetchall()

    conn.commit()
    cur.close()

    return jsonify(result), 200


@ app.route("/check_class_list/<int:class_id>", methods=['GET'])
def check_class_list(class_id):

    conn = mysql.connect()
    cur = conn.cursor()

    cur.execute("""SELECT class_list.emp_id,class_list.class_id,class.course_id,
                    class_list.progress,class_list.class_status,
                    class_list.graded_result FROM course.class_list 
                    INNER JOIN course.class ON class.class_id = class_list.class_id 
                    WHERE class_list.class_id=%s;""", (class_id))
    result = cur.fetchall()

    conn.commit()
    cur.close()

    return jsonify(result), 200


@ app.route("/class_info", methods=['POST'])
def class_info():
    # check for body request
    if not request.json:
        return("Invalid body request."), 400

    class_id = request.json['class_id']

    conn = mysql.connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM course.class WHERE class_id=%s", (class_id))
    result = cur.fetchall()

    conn.commit()
    cur.close()

    return jsonify(result), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
