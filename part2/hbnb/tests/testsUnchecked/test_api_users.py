import unittest
import requests
import uuid
from app import create_app
import json

BASE_URL = 'http://127.0.0.1:5000/api/v1/users'

class TestUserAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user_data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "testuser@example.com"
        }
        cls.update_data = {
            "first_name": "Updated",
            "last_name": "User",
            "email": "updateduser@example.com"
        }

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

    def test_post_user_valid(self):
        unique_email = f"testuser_{uuid.uuid4()}@example.com"
        user_data = {
            "first_name": self.user_data["first_name"],
            "last_name": self.user_data["last_name"],
            "email": unique_email
        }
        response = requests.post(BASE_URL + '/', json=user_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json())
        TestUserAPI.user_id = response.json()['id']

    def test_post_user_invalid(self):
        # Empty fields
        bad_data = {"first_name": "", "last_name": "", "email": "notanemail"}
        response = requests.post(BASE_URL + '/', json=bad_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())
        # Missing fields
        response = requests.post(BASE_URL + '/', json={"first_name": "OnlyFirst"})
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())
        # Extra fields
        bad_data = {"first_name": "Test", "last_name": "User", "email": "testextra@example.com", "extra": "field"}
        response = requests.post(BASE_URL + '/', json=bad_data)
        self.assertIn(response.status_code, [201, 400])

    def test_post_user_duplicate_email(self):
        # Try to create the same user again
        response = requests.post(BASE_URL + '/', json=self.user_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    def test_get_users(self):
        response = requests.get(BASE_URL + '/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_get_user_by_id_valid(self):
        if not hasattr(TestUserAPI, 'user_id'):
            self.skipTest("No user_id available")
        response = requests.get(f"{BASE_URL}/{TestUserAPI.user_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn('id', response.json())

    def test_get_user_by_id_invalid(self):
        # Not a UUID
        response = requests.get(f"{BASE_URL}/not-a-uuid")
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())
        # Valid UUID but not UUID4
        response = requests.get(f"{BASE_URL}/123e4567-e89b-12d3-a456-426614174000")
        self.assertIn(response.status_code, [400, 404])

    def test_get_user_by_id_not_found(self):
        random_id = str(uuid.uuid4())
        response = requests.get(f"{BASE_URL}/{random_id}")
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.json())

    def test_put_user_valid(self):
        if not hasattr(TestUserAPI, 'user_id'):
            self.skipTest("No user_id available")
        response = requests.put(f"{BASE_URL}/{TestUserAPI.user_id}", json=self.update_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['first_name'], self.update_data['first_name'])

    def test_put_user_invalid_id(self):
        response = requests.put(f"{BASE_URL}/invalid-uuid", json=self.update_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    def test_put_user_not_found(self):
        random_id = str(uuid.uuid4())
        response = requests.put(f"{BASE_URL}/{random_id}", json=self.update_data)
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.json())

    def test_put_user_invalid_data(self):
        if not hasattr(TestUserAPI, 'user_id'):
            self.skipTest("No user_id available")
        # Empty fields
        bad_data = {"first_name": "", "last_name": "", "email": "bademail"}
        response = requests.put(f"{BASE_URL}/{TestUserAPI.user_id}", json=bad_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())
        # Missing fields
        response = requests.put(f"{BASE_URL}/{TestUserAPI.user_id}", json={"first_name": "OnlyFirst"})
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())
        # Extra fields
        bad_data = {"first_name": "Test", "last_name": "User", "email": "testextra2@example.com", "extra": "field"}
        response = requests.put(f"{BASE_URL}/{TestUserAPI.user_id}", json=bad_data)
        self.assertIn(response.status_code, [200, 400])

    def test_delete_user_invalid_id(self):
        # If you have a DELETE endpoint, test invalid id
        response = requests.delete(f"{BASE_URL}/invalid-uuid")
        self.assertIn(response.status_code, [400, 404])

if __name__ == "__main__":
    unittest.main()
