import unittest
from app.models.review import Review
from app.models.place import Place
from app.models.user import User


class TestReview(unittest.TestCase):
    def setUp(self):
        self.user = User(first_name="John", last_name="Doe",
                         email="john@doe.com", is_admin=False)
        self.place = Place(title="Test Place", description="A place",
                           price=10.0, latitude=0.0, longitude=0.0,
                           owner=self.user)
        self.valid_data = {
            'text': 'Great place!',
            'rating': 5,
            'place': self.place,
            'user': self.user
        }

    def test_review_creation_valid(self):
        review = Review(**self.valid_data)
        self.assertEqual(review.text, self.valid_data['text'])
        self.assertEqual(review.rating, self.valid_data['rating'])
        self.assertEqual(review.place, self.place)
        self.assertEqual(review.user, self.user)
        self.assertIn(review, self.place.reviews)

    def test_missing_required_fields(self):
        with self.assertRaises(ValueError):
            Review(text='', rating=5, place=self.place, user=self.user)
        with self.assertRaises(ValueError):
            Review(text='Nice', rating=None, place=self.place,
                   user=self.user)
        with self.assertRaises(ValueError):
            Review(text='Nice', rating=5, place=None, user=self.user)
        with self.assertRaises(ValueError):
            Review(text='Nice', rating=5, place=self.place, user=None)

    def test_invalid_text_type_and_length(self):
        with self.assertRaises(TypeError):
            Review(text=123, rating=5, place=self.place, user=self.user)
        with self.assertRaises(ValueError):
            Review(text='A', rating=5, place=self.place, user=self.user)
        with self.assertRaises(ValueError):
            Review(text='A'*501, rating=5, place=self.place, user=self.user)

    def test_invalid_rating_type_and_range(self):
        with self.assertRaises(TypeError):
            Review(text='Nice', rating='bad', place=self.place, user=self.user)
        with self.assertRaises(ValueError):
            Review(text='Nice', rating=0, place=self.place, user=self.user)
        with self.assertRaises(ValueError):
            Review(text='Nice', rating=6, place=self.place, user=self.user)

    def test_invalid_place_and_user_type(self):
        with self.assertRaises(TypeError):
            Review(text='Nice', rating=5, place='not_a_place', user=self.user)
        with self.assertRaises(TypeError):
            Review(text='Nice', rating=5, place=self.place, user='not_a_user')

    def test_review_added_to_place(self):
        review = Review(text='Another review', rating=4,
                        place=self.place, user=self.user)
        self.assertIn(review, self.place.reviews)
        self.assertEqual(len(self.place.reviews), 1)


if __name__ == "__main__":
    unittest.main()
