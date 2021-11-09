from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root' + \
    '@127.0.0.1:3306/course'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100,
                                           'pool_recycle': 280}

CORS(app)
db = SQLAlchemy(app)


class Class_List(db.Model):
    __tablename__ = 'class_list'
    emp_id = db.Column(db.Integer, primary_key=True)
    emp_name = db.Column(db.String(255))
    class_id = db.Column(db.Integer)
    progress = db.Column(db.String(255))
    class_status = db.Column(db.String(255))
    ungraded_result = db.Column(db.String(255))
    graded_result = db.Column(db.String(255))

    def to_dict(self):
        """
        'to_dict' converts the object into a dictionary,
        in which the keys correspond to database columns
        """
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result

    def class_id(self):
        return self._class_id
    
class Class_List(db.Model):
    __tablename__ = 'class_list'
    emp_id = db.Column(db.Integer, primary_key=True)
    emp_name = db.Column(db.String(255))
    class_id = db.Column(db.Integer)
    progress = db.Column(db.String(255))
    class_status = db.Column(db.String(255))
    ungraded_result = db.Column(db.String(255))
    graded_result = db.Column(db.String(255))

    def to_dict(self):
        """
        'to_dict' converts the object into a dictionary,
        in which the keys correspond to database columns
        """
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result

    def class_id(self):
        return self._class_id

class Section(db.Model): 
    __tablename__ = 'section'
    
    section_id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer)
    course_id = db.Column(db.Integer)
    course_name = db.Column(db.String(255))
    section_desc = db.Column(db.String(255))
    materials = db.Column(db.String(255))
 

    def to_dict(self):
        """
        'to_dict' converts the object into a dictionary,
        in which the keys correspond to database columns
        """
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result


db.create_all()

@app.route("/insert_class_list", methods=['POST'])
def insert_class_list():
    data = request.get_json()
    if not all(key in data.keys() for
               key in ('emp_id','emp_name',
                       'class_id','progress','class_status','ungraded_result',
                       'graded_result')):
        return jsonify({
            "message": "Incorrect JSON object provided."
        }), 500
    class_list = Class_List(
        emp_id = data['emp_id'],
        emp_name = data['emp_name'],
        class_id = data['class_id'],
        progress = data['progress'],
        class_status = data['class_status'],
        ungraded_result = data['ungraded_result'],
        graded_result = data['graded_result']
    )
    
    try:
        db.session.add(class_list)
        db.session.commit()
        return jsonify(class_list.to_dict()), 201
    except Exception:
        return jsonify({
            "message": "Unable to commit to database."
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)