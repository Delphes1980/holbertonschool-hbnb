import unittest
import requests
import uuid

BASE_URL = 'http://127.0.0.1:5000/api/v1/amenities'

class TestAmenityAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.amenity_data = {"name": "Wi-Fi"}
        cls.update_data = {"name": "Pool"}

    def test_post_amenity_valid(self):
        response = requests.post(BASE_URL + '/', json=self.amenity_data)
        self.assertIn(response.status_code, [201, 400])
        if response.status_code == 201:
            self.assertIn('id', response.json())
            TestAmenityAPI.amenity_id = response.json()['id']
        else:
            self.assertIn('error', response.json())

    def test_post_amenity_invalid(self):
        bad_data = {"name": ""}
        response = requests.post(BASE_URL + '/', json=bad_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    def test_get_amenities(self):
        response = requests.get(BASE_URL + '/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_get_amenity_by_id_valid(self):
        if not hasattr(TestAmenityAPI, 'amenity_id'):
            self.skipTest("No amenity_id available")
        response = requests.get(f"{BASE_URL}/{TestAmenityAPI.amenity_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn('id', response.json())

    def test_get_amenity_by_id_invalid(self):
        response = requests.get(f"{BASE_URL}/invalid-uuid")
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    def test_get_amenity_by_id_not_found(self):
        random_id = str(uuid.uuid4())
        response = requests.get(f"{BASE_URL}/{random_id}")
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.json())

    def test_put_amenity_valid(self):
        if not hasattr(TestAmenityAPI, 'amenity_id'):
            self.skipTest("No amenity_id available")
        response = requests.put(f"{BASE_URL}/{TestAmenityAPI.amenity_id}", json=self.update_data)
        self.assertIn(response.status_code, [200, 400])
        if response.status_code == 200:
            self.assertEqual(response.json()['name'], self.update_data['name'])
        else:
            self.assertIn('error', response.json())

    def test_put_amenity_invalid_id(self):
        response = requests.put(f"{BASE_URL}/invalid-uuid", json=self.update_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    def test_put_amenity_not_found(self):
        random_id = str(uuid.uuid4())
        response = requests.put(f"{BASE_URL}/{random_id}", json=self.update_data)
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.json())

    def test_put_amenity_invalid_data(self):
        if not hasattr(TestAmenityAPI, 'amenity_id'):
            self.skipTest("No amenity_id available")
        bad_data = {"name": ""}
        response = requests.put(f"{BASE_URL}/{TestAmenityAPI.amenity_id}", json=bad_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

if __name__ == "__main__":
    unittest.main()
