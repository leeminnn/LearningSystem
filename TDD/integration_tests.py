import unittest
import flask_testing
import json
from app import app, db, Quiz


class TestApp(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True

    def create_app(self):
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestUploadQuiz_Success(TestApp):
    def test_create_consultation(self):
        p1 = Quiz(quiz_id=1, section_id=1, class_id=1, course_id=101,
                  total_mark=1, time=60, quiz_type='ungraded')
        db.session.add(p1)
        db.session.commit()

        request_body = {
            'qn_id': 1,
            'quiz_id': p1.quiz_id,
            'quiz_desc': 'Is the Earth Square?',
            'quiz_ans': 'False',
            'question_option': "True,False",
            'mark': 1
        }

        response = self.client.post("/upload_quiz",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.json, {
            'qn_id': 1,
            'quiz_id': 1,
            'quiz_desc': 'Is the Earth Square?',
            'quiz_ans': 'False',
            'question_option': "True,False",
            'mark': 1
        })


class TestUploadQuiz_InvalidRequestBody(TestApp):
    def test_create_consultation(self):
        p1 = Quiz(quiz_id=1, section_id=1, class_id=1, course_id=101,
                  total_mark=1, time=60, quiz_type='ungraded')
        db.session.add(p1)
        db.session.commit()

        request_body = {
            'qn_id': 1,
            'quiz_desc': 'Is the Earth Square?',
            'quiz_ans': 'False',
            'question_option': "True,False",
            'mark': 1
        }

        response = self.client.post("/upload_quiz",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message': 'Incorrect JSON object provided.'
        })


if __name__ == '__main__':
    unittest.main()
