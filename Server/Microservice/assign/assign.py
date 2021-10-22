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
app.config['MYSQL_DATABASE_DB'] = 'section'

mysql = MySQL(app, cursorclass=DictCursor)
mysql.init_app(app)


@app.route('/hi', methods=['POST'])
def hi():

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""SELECT * FROM section.section""")
    result = cur.fetchall()

    return jsonify({'data': result}), 200


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
    cur.execute("INSERT INTO pending_enrolment(emp_id, course_id, class_id, status) VALUES (%s, %s, %s, %s)",
                (emp_id, course_id, class_id, status))

    # commit the command
    conn.commit()

    # close sql connection
    cur.close()

    return("Success"), 200


@app.route('/assign', methods=['POST'])
def assign():

    # check for body request
    if not request.json:
        return("Invalid body request."), 400

    emp_id = request.json['emp_id']
    course_id = request.json['course_id']
    class_id = request.json['class_id']
    status = request.json['status']
    progress = request.json['progress']

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO learner_list(emp_id, class_id, status, progress) VALUES (%s, %s, %s, %s)",
                (emp_id, class_id, status, progress))
    cur.execute(
        "DELETE FROM pending_enrolment WHERE emp_id=%s and course_id=%s and class_id=%s", [emp_id, course_id, class_id])

    # commit the command
    conn.commit()
    cur.close()

    return("Success"), 200


# HR withdraw students
@app.route('/withdraw', methods=['DELETE'])
def withdraw():

    if not request.json:
        return("Invalid body request."), 400

    user = request.json['user']

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM Quiz WHERE user=%s", [user])
    conn.commit()
    cur.close()

    return("Success"), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5100, debug=True)
