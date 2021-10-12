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
app.config['MYSQL_DATABASE_DB'] = 'employee'

mysql = MySQL(app, cursorclass=DictCursor)
mysql.init_app(app)


@app.route("/employee", methods=['GET'])
def get_all():
            # check for body request
    if not request.json:
        return("Invalid body request."), 400

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""SELECT * FROM employee""")
    result = cur.fetchall()
    conn.commit()
    cur.close()


    return jsonify(result), 203


@app.route("/get_one", methods=['GET'])
def get_one():
                # check for body request
    if not request.json:
        return("Invalid body request."), 400

    emp = request.json['emp_id']

    conn = mysql.connect()
    cur = conn.cursor()

    cur.execute("""SELECT * FROM employee WHERE emp_id=%s""", (emp))

    conn.commit()
    cur.close()


    return ("Success"), 203

@app.route('/update_employee', methods=['PUT']) 
def update_employee():
    #check for body request
    if not request.json:
        return ("Invalid body request."),400

    emp_id = request.json['emp_id']
    emp_name = request.json['emp_name']
    email = request.json['email']
    phone = request.json['phone']
    dept = request.json['dept']

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""UPDATE course.course SET emp_name = %s, email = %s , phone =%s, dept=%s
                WHERE emp_id = %s """,
                (emp_name, email, phone, dept,emp_id))

    # commit the command
    conn.commit()

    # close sql connection
    cur.close()

    return("Successfully Update employee information"), 201

@app.route('/add_employee', methods=['POST']) 
def add_employee():
    #check for body request
    if not request.json:
        return("Invalid body request."), 400
    
    emp_id = request.json['emp_id']
    emp_name = request.json['emp_name']
    email = request.json['email']
    phone = request.json['phone']
    dept = request.json['dept']

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""INSERT INTO course.class(emp_id,emp_name,email,phone,dept) VALUES (%s, %s, %s, %s, %s)""",
                (emp_id,emp_name,email,phone,dept))    # commit the command
    conn.commit()

    # close sql connection
    cur.close()

    return("Successfully added employee"), 201


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
