import unittest
import requests

BASE_URL = 'http://127.0.0.1:5000/api/v1/users'

class TestUserAPI(unittest.TestCase):
    user_id = None  # Initialize as class attribute

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

    def test_01_post_user(self):
        response = requests.post(BASE_URL + '/', json=self.user_data)
        self.assertIn(response.status_code, [201, 400])  # 400 if already exists
        if response.status_code == 201:
            self.assertIn('id', response.json())
        else:
            self.assertIn('error', response.json())

    def test_02_post_user_duplicate_email(self):
        response = requests.post(BASE_URL + '/', json=self.user_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    def test_03_get_users(self):
        response = requests.get(BASE_URL + '/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        if response.json():
            TestUserAPI.user_id = response.json()[0]["id"]
        else:
            TestUserAPI.user_id = None

    def test_04_get_user_by_id(self):
        if not TestUserAPI.user_id:
            self.skipTest("No user_id available")
        response = requests.get(f"{BASE_URL}/{TestUserAPI.user_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn('id', response.json())

    def test_05_get_user_invalid_id(self):
        response = requests.get(f"{BASE_URL}/invalid-uuid")
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    def test_06_get_user_not_found(self):
        import uuid
        random_id = str(uuid.uuid4())
        response = requests.get(f"{BASE_URL}/{random_id}")
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.json())

    def test_07_put_user(self):
        if not TestUserAPI.user_id:
            self.skipTest("No user_id available")
        response = requests.put(f"{BASE_URL}/{TestUserAPI.user_id}", json=self.update_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['first_name'], self.update_data['first_name'])

    def test_08_put_user_invalid_id(self):
        response = requests.put(f"{BASE_URL}/invalid-uuid", json=self.update_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    def test_09_put_user_not_found(self):
        import uuid
        random_id = str(uuid.uuid4())
        response = requests.put(f"{BASE_URL}/{random_id}", json=self.update_data)
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.json())

    def test_10_put_user_duplicate_email(self):
        # Create a second user
        second_user = {
            "first_name": "Second",
            "last_name": "User",
            "email": "seconduser@example.com"
        }
        requests.post(BASE_URL + '/', json=second_user)
        if not TestUserAPI.user_id:
            self.skipTest("No user_id available")
        # Try to update first user to have the same email as second user
        response = requests.put(f"{BASE_URL}/{TestUserAPI.user_id}", json=second_user)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

if __name__ == "__main__":
    unittest.main()

    # --- Original script for manual API testing ---
    import json
    
    user_data = {
        "first_name": "Test",
        "last_name": "User",
        "email": "testuser@example.com"
    }
    update_data = {
        "first_name": "Updated",
        "last_name": "User",
        "email": "updateduser@example.com"
    }
    def test_post_user():
        print("Testing POST /users/")
        response = requests.post(BASE_URL + '/', json=user_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    def test_get_users():
        print("Testing GET /users/")
        response = requests.get(BASE_URL + '/')
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        if response.json():
            return response.json()[0]["id"]
        return None
    def test_get_user_by_id(user_id):
        print(f"Testing GET /users/{{user_id}} with id={user_id}")
        response = requests.get(f"{BASE_URL}/{user_id}")
        print(f"Status: {response.status_code}")
        try:
            print(f"Response: {response.json()}")
        except Exception:
            print(f"Response: {response.text}")
    def test_put_user(user_id):
        print(f"Testing PUT /users/{{user_id}} with id={user_id}")
        response = requests.put(f"{BASE_URL}/{user_id}", json=update_data)
        print(f"Status: {response.status_code}")
        try:
            print(f"Response: {response.json()}")
        except Exception:
            print(f"Response: {response.text}")
    print("\n--- Manual API Testing Script ---")
    test_post_user()
    user_id = test_get_users()
    if user_id:
        test_get_user_by_id(user_id)
        test_put_user(user_id)
        test_get_user_by_id(user_id)
    else:
        print("No users found to test GET/PUT /users/<user_id>")
