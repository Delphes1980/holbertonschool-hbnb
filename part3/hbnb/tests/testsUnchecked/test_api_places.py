import unittest
import requests
import uuid

BASE_URL = 'http://127.0.0.1:5000/api/v1/places'

class TestPlaceAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # You may want to create a user first and use its ID as owner
        cls.owner_id = None
        user_resp = requests.post('http://127.0.0.1:5000/api/v1/users/', json={
            "first_name": "Owner",
            "last_name": "Test",
            "email": "owner.place@example.com"
        })
        if user_resp.status_code == 201:
            cls.owner_id = user_resp.json()['id']
        cls.place_data = {
            "title": "Test Place",
            "description": "A nice place",
            "price": 100,
            "latitude": 10.0,
            "longitude": 20.0,
            "owner": cls.owner_id
        }
        cls.update_data = {
            "title": "Updated Place",
            "description": "Updated description",
            "price": 200,
            "latitude": 15.0,
            "longitude": 25.0,
            "owner": cls.owner_id
        }

    def test_post_place_valid(self):
        response = requests.post(BASE_URL + '/', json=self.place_data)
        self.assertIn(response.status_code, [201, 400])
        if response.status_code == 201:
            self.assertIn('id', response.json())
            TestPlaceAPI.place_id = response.json()['id']
        else:
            self.assertIn('error', response.json())

    def test_post_place_invalid(self):
        bad_data = {"title": "", "price": -1, "latitude": 200, "longitude": 200, "owner": ""}
        response = requests.post(BASE_URL + '/', json=bad_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    def test_get_places(self):
        response = requests.get(BASE_URL + '/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_get_place_by_id_valid(self):
        if not hasattr(TestPlaceAPI, 'place_id'):
            self.skipTest("No place_id available")
        response = requests.get(f"{BASE_URL}/{TestPlaceAPI.place_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn('id', response.json())

    def test_get_place_by_id_invalid(self):
        response = requests.get(f"{BASE_URL}/invalid-uuid")
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    def test_get_place_by_id_not_found(self):
        random_id = str(uuid.uuid4())
        response = requests.get(f"{BASE_URL}/{random_id}")
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.json())

    def test_put_place_valid(self):
        if not hasattr(TestPlaceAPI, 'place_id'):
            self.skipTest("No place_id available")
        response = requests.put(f"{BASE_URL}/{TestPlaceAPI.place_id}", json=self.update_data)
        self.assertIn(response.status_code, [200, 400])
        if response.status_code == 200:
            self.assertEqual(response.json()['title'], self.update_data['title'])
        else:
            self.assertIn('error', response.json())

    def test_put_place_invalid_id(self):
        response = requests.put(f"{BASE_URL}/invalid-uuid", json=self.update_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    def test_put_place_not_found(self):
        random_id = str(uuid.uuid4())
        response = requests.put(f"{BASE_URL}/{random_id}", json=self.update_data)
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.json())

    def test_put_place_invalid_data(self):
        if not hasattr(TestPlaceAPI, 'place_id'):
            self.skipTest("No place_id available")
        bad_data = {"title": "", "price": -1, "latitude": 200, "longitude": 200, "owner": ""}
        response = requests.put(f"{BASE_URL}/{TestPlaceAPI.place_id}", json=bad_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

if __name__ == "__main__":
    unittest.main()
