from app.persistence.repository import InMemoryRepository
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.user import User
from app.models.review import Review


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def create_amenity(self, amenity_data):
        # Validate the amenity data
        new_amenity = Amenity(**amenity_data)
        # Store the new amenity in the repository
        self.amenity_repo.add(new_amenity)
        return new_amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity_to_update = self.amenity_repo.get(amenity_id)
        # Check if amenity exists
        if not amenity_to_update:
            return None
        # Update the amenity with the provided data
        amenity_to_update.update(amenity_data)
        updated_amenity = self.amenity_repo.get(amenity_id)
        return updated_amenity
