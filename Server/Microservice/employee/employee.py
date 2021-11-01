from pymysql import NULL
from flask import jsonify, Flask, request
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app)

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3305
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'employee'

mysql = MySQL(app, cursorclass=DictCursor)
mysql.init_app(app)


@app.route("/login", methods=['POST'])
def login():
    # check for body request
    if not request.json:
        return("Invalid body request."), 400

    emp_id = request.json['emp_id']
    password = request.json['password']

    conn = mysql.connect()
    cur = conn.cursor()

    cur.execute(
        """SELECT emp_password, emp_name FROM employee.employee WHERE emp_id=%s""", (emp_id))
    result = cur.fetchall()
    conn.commit()
    cur.close()
    if password != result[0]['emp_password']:
        return ("Not Successful"), 401
    return result[0]['emp_name'], 200


@app.route("/get_learners", methods=['POST'])
def get_learners():

    if not request.json:
        return("Invalid body request."), 400

    course_id = request.json['course_id']
    final = []

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute(
        """SELECT pre_req FROM course.course WHERE course_id=%s""", (course_id))
    res = cur.fetchall()
    if res[0]['pre_req'] != "No Prerequisite Course":
        pre_req = str(res[0]['pre_req'])
    else:
        pre_req = course_id

    cur.execute("""SELECT * FROM employee.learner""")
    result = cur.fetchall()
    for i in result:
        i['emp_id'] = str(i['emp_id']).rjust(3, '0')
        if i['courses_ongoing'] != None:
            courseID = i['courses_ongoing'].split(',')
        else:
            courseID = []
        if i['courses_completed'] != None:
            ccourseID = i['courses_completed'].split(',')
        else:
            ccourseID = []
        if (course_id not in courseID) and (course_id not in ccourseID):
            if pre_req != "No Prerequisite Course" and (pre_req in ccourseID):
                final.append(i)
            else:
                final.append(i)

    conn.commit()

    cur.close()

    return jsonify(final), 200


@app.route("/get_trainers", methods=['GET'])
def get_trainers():

    conn = mysql.connect()
    cur = conn.cursor()

    cur.execute("""SELECT emp_id,emp_name FROM employee.trainer""")

    result = cur.fetchall()

    for i in result:
        i['emp_id'] = str(i['emp_id']).rjust(3, '0')
    conn.commit()
    cur.close()

    return jsonify(result), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
