from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root' + \
    '@3.18.143.100:3306/section'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100,
                                           'pool_recycle': 280}

CORS(app)
db = SQLAlchemy(app)


class Quiz(db.Model):
    __tablename__ = 'quiz'
    quiz_id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer)
    class_id = db.Column(db.Integer)
    course_id = db.Column(db.Integer)
    total_mark = db.Column(db.Integer)
    time = db.Column(db.Integer)
    quiz_type = db.Column(db.String(100))

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

    def quizID(self):
        return self._quiz_id


class Question(db.Model):
    __tablename__ = 'question'

    qn_id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer)
    quiz_desc = db.Column(db.String(100))
    quiz_ans = db.Column(db.String(100))
    question_option = db.Column(db.String(100))
    mark = db.Column(db.Integer)

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


@app.route("/upload_quiz", methods=['POST'])
def upload_quiz():
    data = request.get_json()
    if not all(key in data.keys() for
               key in ('qn_id', 'quiz_id',
                       'quiz_desc', 'quiz_ans', 'question_option', 'mark')):
        return jsonify({
            "message": "Incorrect JSON object provided."
        }), 500

    question = Question(
        qn_id=data['qn_id'],
        quiz_id=data['quiz_id'],
        quiz_desc=data['quiz_desc'],
        quiz_ans=data['quiz_ans'],
        question_option=data['question_option'],
        mark=data['mark']
    )

    try:
        db.session.add(question)
        db.session.commit()
        return jsonify(question.to_dict()), 201
    except Exception:
        return jsonify({
            "message": "Unable to commit to database."
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
