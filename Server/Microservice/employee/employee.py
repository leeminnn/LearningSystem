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

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""SELECT * FROM employee""")
    result = cur.fetchall()

    return jsonify(result), 203


@app.route("/employee/<int:emp>", methods=['GET'])
def get_one(emp):

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""SELECT * FROM employee WHERE emp_id=%s""", [emp])
    result = cur.fetchall()

    return jsonify(result), 203


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
