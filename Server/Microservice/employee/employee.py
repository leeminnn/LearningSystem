import requests
import datetime
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
        """SELECT password, emp_name FROM employee.employee WHERE emp_id=%s""", (emp_id))
    result = cur.fetchall()
    conn.commit()
    cur.close()
    if password != result[0]['password']:
        return ("Not Successful"), 401
    return result[0]['emp_name'], 200

# get list all employees


@app.route("/all_employee", methods=['GET'])
def all_employee():

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""SELECT * FROM employee.employee""")
    result = cur.fetchall()
    for i in result:
        i['emp_id'] = str(i['emp_id']).rjust(3, '0')
    conn.commit()
    cur.close()

    return jsonify(result), 200


@app.route("/get_learners", methods=['GET'])
def get_learners():

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""SELECT * FROM employee.learner""")
    result = cur.fetchall()
    for i in result:
        i['emp_id'] = str(i['emp_id']).rjust(3, '0')
    conn.commit()
    cur.close()

    return jsonify(result), 200

# get all information of 1 employee


@app.route("/get_one", methods=['POST'])
def get_one():
    # check for body request
    if not request.json:
        return("Invalid body request."), 400

    emp_id = request.json['emp_id']

    conn = mysql.connect()
    cur = conn.cursor()

    cur.execute("""SELECT * FROM employee.employee WHERE emp_id=%s""", (emp_id))

    result = cur.fetchall()
    conn.commit()
    cur.close()

    return jsonify(result), 200

# get employee name when type id


@app.route("/get_emp_name", methods=['POST'])
def get_emp_name():
    # check for body request
    if not request.json:
        return("Invalid body request."), 400

    emp_id = request.json['emp_id']

    conn = mysql.connect()
    cur = conn.cursor()

    cur.execute(
        """SELECT emp_id,emp_name FROM employee.employee WHERE emp_id=%s""", (emp_id))

    result = cur.fetchall()
    conn.commit()
    cur.close()

    return jsonify(result), 200

# get all trainers id name


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


# update employee information
@app.route('/update_employee', methods=['PUT'])
def update_employee():
    # check for body request
    if not request.json:
        return ("Invalid body request."), 400

    emp_id = request.json['emp_id']
    emp_name = request.json['emp_name']
    email = request.json['email']
    phone = request.json['phone']
    dept = request.json['dept']

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""UPDATE employee.employee SET emp_name = %s, email = %s , phone =%s, dept=%s
                WHERE emp_id = %s """,
                (emp_name, email, phone, dept, emp_id))

    # commit the command
    conn.commit()

    # close sql connection
    cur.close()

    return("Successfully Update employee information"), 200

# add new employee


@app.route('/add_employee', methods=['POST'])
def add_employee():
    # check for body request
    if not request.json:
        return("Invalid body request."), 400

    emp_id = request.json['emp_id']
    emp_name = request.json['emp_name']
    email = request.json['email']
    phone = request.json['phone']
    dept = request.json['dept']

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""INSERT INTO employee.employee(emp_id,emp_name,email,phone,dept) VALUES (%s, %s, %s, %s, %s)""",
                (emp_id, emp_name, email, phone, dept))
    # commit the command
    conn.commit()

    # close sql connection
    cur.close()

    return("Successfully added employee"), 200

# insert new trainer


@app.route('/add_trainer', methods=['POST'])
def add_trainer():
    # check for body request
    if not request.json:
        return("Invalid body request."), 400

    emp_id = request.json['emp_id']
    emp_name = request.json['emp_name']
    courses_teaching = request.json['courses_teaching']
    courses_completed = request.json['courses_completed']

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""INSERT INTO employee.trainer(emp_id,emp_name,courses_teaching,courses_completed) VALUES (%s, %s, %s, %s)""",
                (emp_id, emp_name, courses_teaching, courses_completed))
    # commit the command
    conn.commit()

    # close sql connection
    cur.close()
    return("Successfully add new trainer"), 200

# update trainer courses teaching


@app.route('/update_trainer_teaching', methods=['PUT'])
def update_trainer_teaching():
    # check for body request
    if not request.json:
        return("Invalid body request."), 400

    emp_id = request.json['emp_id']
    courses_teaching = request.json['courses_teaching']

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""UPDATE employee.trainer SET courses_teaching = %s
                WHERE emp_id = %s """,
                (courses_teaching, emp_id))
    # commit the command
    conn.commit()

    # close sql connection
    cur.close()

    return("Successfully update courses teaching"), 200

# update trainer courses completed


@app.route('/update_trainer_completed', methods=['PUT'])
def update_trainer_completed():
    # check for body request
    if not request.json:
        return("Invalid body request."), 400

    emp_id = request.json['emp_id']
    courses_completed = request.json['courses_completed']

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""UPDATE employee.trainer SET courses_completed = %s
                WHERE emp_id = %s """,
                (courses_completed, emp_id))
    # commit the command
    conn.commit()

    # close sql connection
    cur.close()

    return("Successfully update courses completed"), 200

# insert new learner


@app.route('/add_learner', methods=['POST'])
def add_learner():
    # check for body request
    if not request.json:
        return("Invalid body request."), 400

    emp_id = request.json['emp_id']
    emp_name = request.json['emp_name']
    courses_ongoing = request.json['courses_ongoing']
    courses_completed = request.json['courses_completed']
    badge = request.json['badge']

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""INSERT INTO employee.learner(emp_id,emp_name,courses_ongoing,courses_completed,badge) VALUES (%s, %s, %s, %s,%s)""",
                (emp_id, emp_name, courses_ongoing, courses_completed, badge))
    # commit the command
    conn.commit()

    # close sql connection
    cur.close()
    return("Successfully add new learner"), 200

# update learner courses_ongoing


@app.route('/update_learner_courses_list', methods=['PUT'])
def update_learner_ongoing():
    # check for body request
    if not request.json:
        return("Invalid body request."), 400
    
    course_id = int(request.json['course_id'])
    emp_id = request.json['emp_id']

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""SELECT courses_ongoing,courses_completed FROM employee.learner WHERE emp_id = %s""",(emp_id))
    result = cur.fetchall()

    courses_ongoing = result[0]["courses_ongoing"].split(',')
    courses_ongoing = list(map(int, courses_ongoing))
    courses_completed = result[0]["courses_completed"].split(',')
    courses_completed = list(map(int, courses_completed))

    for i in courses_ongoing:
        if course_id == i:
            courses_ongoing.remove(i)

    courses_completed.append(course_id)
    courses_ongoing = str(courses_ongoing).strip('][')
    courses_completed = str(courses_completed).strip('][')

    cur.execute("""UPDATE employee.learner SET courses_ongoing = %s, courses_completed = %s WHERE emp_id = %s """,
    (courses_ongoing,courses_completed,emp_id))
    # commit the command
    conn.commit()

    # close sql connection
    cur.close()

    return("successfully updated learner courses"), 200

# update learner courses_badge


@app.route('/update_learner_badge', methods=['PUT'])
def update_learner_badge():
    # check for body request
    if not request.json:
        return("Invalid body request."), 400

    emp_id = request.json['emp_id']
    badge = request.json['badge']

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""UPDATE employee.learner SET badge = %s
                WHERE emp_id = %s """,
                (badge, emp_id))
    # commit the command
    conn.commit()

    # close sql connection
    cur.close()

    return("Successfully update learner badge"), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
