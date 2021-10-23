import requests
import datetime
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

    return jsonify(result), 200


## trainer want to create quiz  ##
@app.route("/create_quiz", methods=['GET'])
def create_quiz():

    # step 1 create row in quiz table
    # step 2 create question rows

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""SELECT * FROM employee WHERE emp_id=%s""", [])
    result = cur.fetchall()

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
        "_section-" + str(section_id) + "_" + str(file_name.filename)

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
    final = []

    conn = mysql.connect()
    cur = conn.cursor()
    if section_id != " ":
        cur.execute("""SELECT quiz_id, total_mark FROM section.quiz WHERE section_id=%s and class_id=%s and course_id=%s""",
                    (section_id, class_id, course_id))
        result = cur.fetchall()
    else:
        cur.execute("""SELECT quiz_id, total_mark FROM section.quiz WHERE quiz_type='graded' and class_id=%s and course_id=%s""",
                    (class_id, course_id))
        result = cur.fetchall()

    for i in result:
        quizID = i['quiz_id']
        cur.execute("""SELECT * FROM section.question WHERE quiz_id=%s""",
                    (quizID))
        details = cur.fetchall()
        if len(details) > 0:
            final.append(details)

    if len(final) > 0:
        final.append(result[0]['total_mark'])

    # commit the command
    conn.commit()

    # close sql connection
    cur.close()

    return jsonify(final), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=True)
