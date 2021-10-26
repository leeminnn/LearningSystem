import requests
import datetime
import random
from flask import jsonify, Flask, request
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
import boto3
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)


app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3305
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'section'

mysql = MySQL(app, cursorclass=DictCursor)
mysql.init_app(app)


## learner want to take the quiz ##
## I need learner score, check the answer with database ##
@app.route("/section_info", methods=['POST'])
def section_info():

    if not request.json:
        return("Invalid body request."), 400

    course_id = request.json['course_id']
    class_id = request.json['class_id']

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute(
        """SELECT * FROM section.section where class_id=%s and course_id=%s""", [class_id, course_id])
    result = cur.fetchall()
    conn.commit()
    cur.close()

    return jsonify(result), 200


## trainer want to create quiz  ##
@app.route("/create_question", methods=['POST'])
def create_quiz():

    if not request.json:
        return("Invalid body request."), 400

    quiz_id = request.json['quiz_id']
    ques_desc = request.json['question']
    quiz_ans = request.json['answer']
    question_option = request.json['question_option']
    mark = request.json['mark']

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""INSERT INTO section.question(quiz_id, quiz_desc, quiz_ans, question_option, mark) VALUES (%s, %s, %s, %s, %s)""",
                (quiz_id, ques_desc, quiz_ans, question_option, mark))
    result = cur.fetchall()
    conn.commit()
    cur.close()

    return jsonify(result), 200


## trainer want to upload materials  ##
@app.route("/upload_materials", methods=['POST'])
def upload_materials():

    file_name = request.files['filename']
    course_id = request.form['course_id']
    class_id = request.form['class_id']
    section_id = request.form['section_id']
    # print(filename)
    key_name = "course_" + str(course_id) + "_class_" + str(class_id) + \
        "_section_" + str(section_id) + "_" + str(file_name.filename)

    s3 = boto3.resource('s3')
    s3.Bucket('coursematerialg5t4').put_object(
        Key=key_name, Body=file_name)

    materials = "https://coursematerialg5t4.s3.amazonaws.com/" + key_name

    conn = mysql.connect()
    cur = conn.cursor()

    cur.execute("""UPDATE section.section SET materials=%s WHERE section_id=%s and class_id=%s and course_id=%s;""",
                (materials, section_id, class_id, course_id))
    conn.commit()
    cur.close()

    return ("https://coursematerialg5t4.s3.amazonaws.com/" + key_name), 200


## trainer want to create section ##
@ app.route('/add_section', methods=['POST'])
def add_section():

    # check for body request
    if not request.json:
        return("Invalid body request."), 400

    section_id = request.json['section_id']
    class_id = request.json['class_id']
    course_id = request.json['course_id']
    materials = request.json['materials']

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO section.section(section_id, class_id, course_id, materials) VALUES (%s, %s, %s, %s)",
                (section_id, class_id, course_id, materials))
    result = cur.fetchall()
    conn.commit()

    cur.execute("""INSERT INTO section.quiz(section_id, class_id, course_id, quiz_type) VALUES (%s, %s, %s, %s)""",
                (int(section_id), int(class_id), int(course_id), 'ungraded'))

    # commit the command
    conn.commit()

    # close sql connection
    cur.close()

    return jsonify(result), 200


@ app.route('/create_first_section', methods=['POST'])
def create_first_section():

    # check for body request
    if not request.json:
        return("Invalid body request."), 400

    section_id = "1"
    class_id = request.json['class_id']
    course_id = request.json['course_id']
    materials = " "
    quiz_id = course_id + class_id + '100'

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO section.section(section_id, class_id, course_id, materials) VALUES (%s, %s, %s, %s)",
                (section_id, class_id, course_id, materials))

    cur.execute("INSERT INTO section.quiz(quiz_id, class_id, course_id, materials) VALUES (%s, %s, %s, %s)",
                (quiz_id, class_id, course_id, materials))
    result = cur.fetchall()

    # commit the command
    conn.commit()

    # close sql connection
    cur.close()

    return jsonify(result), 200


@ app.route('/get_quiz_id', methods=['POST'])
def get_quiz_id():

    # check for body request
    if not request.json:
        return("Invalid body request."), 400

    section_id = request.json['section_id']
    class_id = request.json['class_id']
    course_id = request.json['course_id']
    final = {}

    conn = mysql.connect()
    cur = conn.cursor()
    if section_id != " ":
        cur.execute("""SELECT quiz_id, total_mark FROM section.quiz WHERE quiz_type='ungraded' and section_id=%s and class_id=%s and course_id=%s""",
                    (section_id, class_id, course_id))
        result = cur.fetchall()
        conn.commit()
        cur.close()

    else:
        cur.execute("""SELECT quiz_id, total_mark FROM section.quiz WHERE quiz_type='graded' and class_id=%s and course_id=%s""",
                    (class_id, course_id))
        result = cur.fetchall()
        conn.commit()
        cur.close()

    if len(result) > 0:
        final['quiz_id'] = result[0]['quiz_id']
        final['total_mark'] = result[0]['total_mark']

    return jsonify(final), 200


@ app.route('/get_user_sections', methods=['POST'])
def get_user_sections():

    # check for body request
    if not request.json:
        return("Invalid body request."), 400

    emp_id = request.json['emp_id']
    course_id = request.json['course_id']
    class_id = request.json['class_id']

    conn = mysql.connect()
    cur = conn.cursor()

    cur.execute("""SELECT ungraded_result FROM course.class_list WHERE emp_id=%s and class_id=%s""",
                (emp_id, class_id))
    result = cur.fetchall()

    ungraded_result = result[0]["ungraded_result"].split(',')
    print(ungraded_result)
    # set section_count as a starting point of Section 1 of the class
    section_count = 1
    for i in ungraded_result:
        if int(i) != 0:
            section_count += 1

    cur.execute("""SELECT * FROM section.section where class_id=%s and course_id=%s order by section_id""",
                (class_id, course_id))
    section_result = cur.fetchall()
    conn.commit()
    cur.close()

    if section_count > len(section_result):
        section_count = len(section_result)

    final = []
    for i in range(0, section_count):
        final.append(section_result[i])

    print(final)

    return jsonify(final), 200

# insert default ungraded_result array into class_list, considering the number of existing sections


@ app.route('/declare_ungraded_quiz', methods=['POST'])
def declare_ungraded_quiz():
    # check for body request
    if not request.json:
        return("Invalid body request."), 400

    employee = request.json['emp_id']
    course_id = request.json['course_id']
    class_id = request.json['class_id']

    conn = mysql.connect()
    cur = conn.cursor()

    cur.execute("""SELECT COUNT(*) section_count FROM section.section WHERE course_id=%s and class_id=%s""",
                (course_id, class_id))
    result = cur.fetchall()
    conn.commit()

    ungraded_result = []

    for i in range(result[0]["section_count"]):
        ungraded_result.append(0)
    ungraded_result = str(ungraded_result).strip('][')

    for i in range(len(employee)):
        emp_id = employee[i]
        cur.execute("""UPDATE course.class_list SET ungraded_result=%s WHERE emp_id=%s and class_id=%s""",
                    (ungraded_result, emp_id, class_id))
        result = cur.fetchall()
        conn.commit()

    cur.close()

    return("Successfully update ungraded_quiz list"), 200


@ app.route('/update_progress', methods=['PUT'])
def update_progress():
    # check for body request
    if not request.json:
        return("Invalid body request."), 400

    # upon completing quiz, we get the section_id for the quiz that the user completed
    quiz_section = int(request.json['section_id'])
    emp_id = request.json['emp_id']
    class_id = request.json['class_id']
    course_id = request.json['course_id']

    conn = mysql.connect()
    cur = conn.cursor()

    # get sections of the class
    cur.execute("""SELECT * FROM section.section where class_id=%s and course_id=%s order by section_id""",
                (class_id, course_id))
    section_result = cur.fetchall()

    section_position = 0
    for i in range(0, len(section_result)):
        print(quiz_section)
        print(section_result[i]["section_id"])
        if (section_result[i]["section_id"] == quiz_section):
            break
        else:
            section_position += 1

    print("Section postion " + str(section_position))

    cur.execute("""SELECT * FROM course.class_list WHERE emp_id=%s and class_id=%s""",
                (emp_id, class_id))
    result = cur.fetchall()

    ungraded_result = result[0]["ungraded_result"].split(',')
    ungraded_result = list(map(int, ungraded_result))

    ungraded_result[section_position] = 1

    # update progress
    completed_section = 0
    total_section = 0
    for i in ungraded_result:
        if int(i) == 1:
            completed_section += 1
        total_section += 1

    new_ungraded_result = str(ungraded_result).strip('][')
    updated_progress = (completed_section/total_section)*100

    # insert to database
    cur.execute("""UPDATE course.class_list SET progress=%s,ungraded_result=%s WHERE emp_id=%s and class_id=%s""",
                (updated_progress, new_ungraded_result, emp_id, class_id))
    updated_result = cur.fetchall()
    conn.commit()
    cur.close()

    return ("successfully updated progress"), 200


@ app.route('/get_questions', methods=['POST'])
def get_questions():

    # check for body request
    if not request.json:
        return("Invalid body request."), 400

    quiz_id = request.json['quiz_id']

    conn = mysql.connect()
    cur = conn.cursor()

    cur.execute("""SELECT * FROM section.question WHERE quiz_id=%s""",
                (quiz_id))
    result = cur.fetchall()
    for i in result:
        i['question_option'] = i['question_option'].split(',')
        temp = []
        for j in i['question_option']:
            if j != 'undefined':
                temp.append(j)
        new_temp = random.sample(temp, len(temp))
        i['question_option'] = new_temp

    conn.commit()
    cur.close()

    return jsonify(result), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=True)
