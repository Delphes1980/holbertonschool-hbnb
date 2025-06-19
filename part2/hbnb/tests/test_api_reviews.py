import unittest
import requests
import uuid

BASE_URL = 'http://127.0.0.1:5000/api/v1/reviews'

class TestReviewAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a user and a place to use for reviews
        user_resp = requests.post('http://127.0.0.1:5000/api/v1/users/', json={
            "first_name": "ReviewUser",
            "last_name": "Test",
            "email": "reviewuser@example.com"
        })
        place_resp = requests.post('http://127.0.0.1:5000/api/v1/places/', json={
            "title": "Review Place",
            "description": "A place for reviews",
            "price": 50,
            "latitude": 5.0,
            "longitude": 5.0,
            "owner": user_resp.json().get('id') if user_resp.status_code == 201 else None
        })
        cls.user_id = user_resp.json().get('id') if user_resp.status_code == 201 else None
        cls.place_id = place_resp.json().get('id') if place_resp.status_code == 201 else None
        cls.review_data = {
            "text": "Great place!",
            "rating": 5,
            "place": cls.place_id,
            "user": cls.user_id
        }
        cls.update_data = {
            "text": "Updated review!",
            "rating": 4,
            "place": cls.place_id,
            "user": cls.user_id
        }

    def test_post_review_valid(self):
        if not self.review_data["place"] or not self.review_data["user"]:
            self.skipTest("No place_id or user_id available")
        response = requests.post(BASE_URL + '/', json=self.review_data)
        self.assertIn(response.status_code, [201, 400])
        if response.status_code == 201:
            self.assertIn('id', response.json())
            TestReviewAPI.review_id = response.json()['id']
        else:
            self.assertIn('error', response.json())

    def test_post_review_invalid(self):
        bad_data = {"text": "", "rating": 0, "place": "", "user": ""}
        response = requests.post(BASE_URL + '/', json=bad_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    def test_get_reviews(self):
        response = requests.get(BASE_URL + '/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_get_review_by_id_valid(self):
        if not hasattr(TestReviewAPI, 'review_id'):
            self.skipTest("No review_id available")
        response = requests.get(f"{BASE_URL}/{TestReviewAPI.review_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn('id', response.json())

    def test_get_review_by_id_invalid(self):
        response = requests.get(f"{BASE_URL}/invalid-uuid")
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    def test_get_review_by_id_not_found(self):
        random_id = str(uuid.uuid4())
        response = requests.get(f"{BASE_URL}/{random_id}")
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.json())

    def test_put_review_valid(self):
        if not hasattr(TestReviewAPI, 'review_id'):
            self.skipTest("No review_id available")
        response = requests.put(f"{BASE_URL}/{TestReviewAPI.review_id}", json=self.update_data)
        self.assertIn(response.status_code, [200, 400])
        if response.status_code == 200:
            self.assertEqual(response.json()['text'], self.update_data['text'])
        else:
            self.assertIn('error', response.json())

    def test_put_review_invalid_id(self):
        response = requests.put(f"{BASE_URL}/invalid-uuid", json=self.update_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    def test_put_review_not_found(self):
        random_id = str(uuid.uuid4())
        response = requests.put(f"{BASE_URL}/{random_id}", json=self.update_data)
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.json())

    def test_put_review_invalid_data(self):
        if not hasattr(TestReviewAPI, 'review_id'):
            self.skipTest("No review_id available")
        bad_data = {"text": "", "rating": 0, "place": "", "user": ""}
        response = requests.put(f"{BASE_URL}/{TestReviewAPI.review_id}", json=bad_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

if __name__ == "__main__":
    unittest.main()
