from hbnb.app.models.user import User
from datetime import datetime
import unittest


class TestUser(unittest.TestCase):

    def test_user_creation(self):
        user = User(first_name="John", last_name="Doe",
                    email="john.doe@example.com")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "john.doe@example.com")
        self.assertFalse(user.is_admin)  # Default value
        self.assertIsInstance(user.id, str)
        self.assertIsInstance(user.created_at, datetime)
        self.assertIsInstance(user.updated_at, datetime)

    def test_admin_user_creation(self):
        user = User("Alice", "Smith", "alice@example.com",
                    is_admin=True)
        self.assertTrue(user.is_admin)
        self.assertEqual(user.first_name, "Alice")
        self.assertEqual(user.last_name, "Smith")
        self.assertEqual(user.email, "alice@example.com")
        self.assertIsInstance(user.id, str)
        self.assertIsInstance(user.created_at, datetime)
        self.assertIsInstance(user.updated_at, datetime)

    def test_user_creation_bad_email(self):
        with self.assertRaises(ValueError) as cm:
            User(first_name="Jane", last_name="Doe", email="invalid-email")
        self.assertIn("Invalid email", str(cm.exception))

    def test_missing_first_name(self):
        with self.assertRaises(ValueError) as e:
            User("", "Doe", "john.doe@example.com")
        self.assertIn("First name", str(e.exception))

    def test_missing_last_name(self):
        with self.assertRaises(ValueError) as e:
            User("John", "", "john.doe@example.com")
        self.assertIn("Last name", str(e.exception))

    def test_invalid_email_no_at(self):
        with self.assertRaises(ValueError) as e:
            User("John", "Doe", "johndoeexample.com")
        self.assertIn("Invalid email", str(e.exception))

    def test_invalid_email_empty(self):
        with self.assertRaises(ValueError) as e:
            User("John", "Doe", "")
        self.assertIn("Invalid email", str(e.exception))

    def test_long_first_name(self):
        with self.assertRaises(ValueError) as e:
            User("JohnDuudly do whatever somethin tkind", "Doe",
                 "email@email.com")
        self.assertIn("First name", str(e.exception))

    def test_name_with_accents_and_special_characters(self):
        # Acceptable names with accents, dots, apostrophes, and dashes
        valid_names = [
            "José", "François", "Müller", "Çelik", "Łukasz", "Zoë",
            "Dvořák", "O'Connor", "Jean-Pierre", "Ana-Maria",
            "Dvořák-Smith", "Zoë-Marie", "J.R.R.", "J. K.",
            "Smith-Jones", "D'Arcy", "St. John"
        ]
        for name in valid_names:
            user = User(first_name=name, last_name="Doe",
                        email="test@example.com")
            self.assertEqual(user.first_name, name)
            user = User(first_name="John", last_name=name,
                        email="test@example.com")
            self.assertEqual(user.last_name, name)

        # Names with invalid special characters or numbers should
        # raise ValueError
        invalid_names = [
            "J*hn", "Ann3", "M@rie", "Al/ice", "Bob!", "Eve#", "123",
            "Jean--Pierre", "Jean..Pierre", "Jean''Pierre",
            "Jean.-Pierre", "-Jean", ".Jean", "Jean-", "Jean'", "'Jean"
        ]
        for name in invalid_names:
            with self.assertRaises(ValueError):
                User(first_name=name, last_name="Doe",
                     email="test@example.com")
            with self.assertRaises(ValueError):
                User(first_name="John", last_name=name,
                     email="test@example.com")


if __name__ == "__main__":
    unittest.main()
