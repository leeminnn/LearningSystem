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
@app.route("/section_info", methods=['GET'])
def section_info():

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""SELECT * FROM section.section""")
    result = cur.fetchall()

    return jsonify(result), 203


## trainer want to create quiz  ##
@app.route("/create_quiz", methods=['GET'])
def create_quiz():

    # step 1 create row in quiz table
    # step 2 create question rows

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""SELECT * FROM employee WHERE emp_id=%s""", [])
    result = cur.fetchall()

    return jsonify(result), 203


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

    cur.execute("""UPDATE section.section SET materials=%s WHERE section_id=%s and class_id=%s course_id=%s;""",
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
    section_name = request.json['section_name']
    section_desc = request.json['section_desc']
    class_id = request.json['class_id']
    course_id = request.json['course_id']
    materials = request.json['materials']

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO section.section(section_id, section_name, section_desc, class_id, course_id, materials) VALUES (%s, %s, %s, %s, %s, %s)",
                (section_id, section_name, section_desc, class_id, course_id, materials))

    # commit the command
    conn.commit()

    # close sql connection
    cur.close()

    return("Success"), 201


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=True)
