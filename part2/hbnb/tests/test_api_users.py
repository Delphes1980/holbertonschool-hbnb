import unittest
from app import create_app
import json

class UserApiTestCase(unittest.TestCase):
    def setUp(self):
        app = create_app()
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_create_user_success(self):
        user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com'
        }
        response = self.app.post('/api/v1/users/',
                                 data=json.dumps(user_data),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['first_name'], 'John')
        self.assertEqual(data['last_name'], 'Doe')
        self.assertEqual(data['email'], 'john.doe@example.com')

    def test_create_user_duplicate_email(self):
        user_data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane.smith@example.com'
        }
        # First creation should succeed
        self.app.post('/api/v1/users/',
                      data=json.dumps(user_data),
                      content_type='application/json')
        # Second creation with same email should fail
        response = self.app.post('/api/v1/users/',
                                 data=json.dumps(user_data),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Email already registered')

if __name__ == '__main__':
    unittest.main()
