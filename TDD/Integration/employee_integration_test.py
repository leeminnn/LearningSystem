import unittest
import flask_testing
import json

from sqlalchemy.sql.elements import Null
from employee_integration_class import app, db, Class_List


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


class TestInsertEmployee_Success(TestApp):
    def test_insert_employee(self):
        assign = Class_List(emp_id=13, emp_name='Buck', class_id=1, progress='0',
                            class_status='Ongoing', ungraded_result='0,0,0,0', graded_result='')
        request_body = {
            'emp_id': assign.emp_id,
            'emp_name': assign.emp_name,
            'class_id': assign.class_id,
            'progress': assign.progress,
            'class_status': assign.class_status,
            'ungraded_result': assign.ungraded_result,
            'graded_result': assign.graded_result
        }

        response = self.client.post("/insert_class_list",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.json, {
            'emp_id': 13,
            'emp_name': 'Buck',
            'class_id': 1,
            'progress': '0',
            'class_status': "Ongoing",
            'ungraded_result': '0,0,0,0',
            'graded_result': ''
        })

    def test_insert_class_failed(self):
        assign = Class_List(emp_id=20, emp_name='Jessie', class_id=1, progress='0',
                            class_status='Ongoing', ungraded_result='0,0,0,0', graded_result='')
        db.session.add(assign)
        db.session.commit()

        request_body = {
            'emp_id': assign.emp_id,
            'emp_name': assign.emp_name,
            'progess': assign.progress
        }

        response = self.client.post("/insert_class_list",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message': 'Incorrect JSON object provided.'
        })


if __name__ == '__main__':
    unittest.main()
