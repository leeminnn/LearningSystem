import requests
import datetime
from flask import jsonify, Flask, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3305
app.config['MYSQL_USER'] = 'user'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'CourseMaterials'

mysql = MySQL(app)


@app.route('/enrol', methods=['POST'])
def enrol():

    if not request.json:
        return("Invalid body request."), 400

    user = request.json['user']
    occupation = request.json['occupation']
    status = request.json['status']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO Quiz(user, occupation, status) VALUES (%s, %s, %s)",
                (user, occupation, status))
    mysql.connection.commit()
    cur.close()

    return("Success"), 201


@app.route('/withdraw', methods=['DELETE'])
def withdraw():

    if not request.json:
        return("Invalid body request."), 400

    user = request.json['user']

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Quiz WHERE user=%s", [user])
    mysql.connection.commit()
    cur.close()

    return("Success"), 202


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
