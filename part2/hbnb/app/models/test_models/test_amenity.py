import unittest
from hbnb.app.models.amenity import Amenity


class TestAmenity(unittest.TestCase):
    def test_amenity_creation_valid(self):
        amenity = Amenity("Wi-Fi")
        self.assertEqual(amenity.name, "Wi-Fi")

    def test_amenity_name_type(self):
        with self.assertRaises(TypeError):
            Amenity(123)
        with self.assertRaises(TypeError):
            Amenity(None)

    def test_amenity_name_length(self):
        with self.assertRaises(ValueError):
            Amenity("")
        with self.assertRaises(ValueError):
            Amenity("A" * 51)

    def test_amenity_name_strip(self):
        amenity = Amenity("  Pool  ")
        self.assertEqual(amenity.name, "Pool")


if __name__ == "__main__":
    unittest.main()
