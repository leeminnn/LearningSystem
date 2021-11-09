import unittest
import flask_testing
import json
from test_assign import app, db, Class_List


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
        
    assign = Class_List(emp_id=2,emp_name='Buck',class_id=1,progress='0',class_status='Ongoing',ungraded_result='0,0,0,0',graded_result='')

    def test_insert_employee(self,assign):
        request_body= {
            'emp_id': assign.emp_id,
            'emp_name': assign.emp_name,
            'class_id' :assign.class_id,
            'progress' :assign.progress,
            'class_status' :assign.class_status,
            'ungraded_result' :assign.ungraded_result,
            'graded_result' :assign.graded_result
            
        }
    
        response = self.client.post("/insert_class_list",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.json, {
            'emp_id': 2,
            'emp_name': 'Buck',
            'class_id': 1,
            'progress': '0',
            'class_status': "Ongoing",
            'ungraded_result' : '0,0,0,0',
            'graded_result': ''
        })


if __name__ == '__main__':
    unittest.main()
