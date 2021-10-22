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


## learner want to take the quiz ##
## I need learner score, check the answer with database ##
@app.route("/get_score", methods=['POST'])
def get_score():

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""SELECT * FROM employee""")
    result = cur.fetchall()

    return jsonify(result), 200


## trainer want to create quiz  ##
@app.route("/create_quiz", methods=['POST'])
def create_quiz():

    # step 1 create row in quiz table
    # step 2 create question rows

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""SELECT * FROM employee WHERE emp_id=%s""", [])
    result = cur.fetchall()

    return jsonify(result), 200


## trainer want to create section ##
@app.route('/add_section', methods=['POST'])
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

    return("Success"), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=True)
