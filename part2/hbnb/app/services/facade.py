from app.persistence.repository import InMemoryRepository
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.user import User
from app.models.review import Review
from uuid import UUID


def is_valid_uuid4(uuid_str):
    """Determines if given str is a uuid4"""
    try:
        val = UUID(uuid_str, version=4)
        return val.version == 4
    except ValueError:
        return False


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

#### Services for Place CRUD operations ####

    def create_place(self, place_data):
        """ Create a new place with the provided data """
        # Check if the owner exists
        if 'owner_id' in place_data:
            owner = self.user_repo.get(place_data['owner_id'])
            if not owner:
                raise ValueError("Owner does not exist")
            # Delete owner_id from place_data if it's not needed for the Place model
            place_data['owner'] = place_data.pop('owner_id')
        # Delete amenities from place_data if they aren't needed for the Place model
        place_data.pop('amenities', None)
        # Validate the place data
        new_place = Place(**place_data)
        # Store the new place in the repository
        self.place_repo.add(new_place)
        return new_place

    def get_place(self, place_id):
        """ Retrieve a place by its ID """
        place = self.place_repo.get(place_id)
        if not place:
            return None
        place.amenities = self.amenity_repo.get_all()
        place.owner = self.user_repo.get(place.owner_id)
        return place

    def get_all_places(self):
        """ Retrieve all places """
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """ Update a place with the provided data """
        place_to_update = self.place_repo.get(place_id)
        # Check if place exists
        if not place_to_update:
            return None
        # Update the place with the provided data
        place_to_update.update(place_data)
        updated_place = self.place_repo.get(place_id)
        return updated_place

#### Services for User CRUD operations ####

    def create_user(self, user_data):
        """ Create a new user with the provided data """
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """ Retrieve a user by their ID """
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """ Retrieve a user byt their email address """
        return self.user_repo.get_by_attribute('email', email)

#### Services for Amenity CRUD operations ####

    def create_amenity(self, amenity_data):
        """ Create a new amenity with the provided data """
        # Validate the amenity data
        new_amenity = Amenity(**amenity_data)
        # Store the new amenity in the repository
        self.amenity_repo.add(new_amenity)
        return new_amenity

    def get_amenity(self, amenity_id):
        """ Retrieve an amenity by its ID """
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """ Retrieve all amenities """
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """ Update an amenity with the provided data """
        amenity_to_update = self.amenity_repo.get(amenity_id)
        # Check if amenity exists
        if not amenity_to_update:
            return None
        # Update the amenity with the provided data
        amenity_to_update.update(amenity_data)
        updated_amenity = self.amenity_repo.get(amenity_id)
        return updated_amenity

#### Services for Review CRUD operations ####

    def create_review(self, review_data):
        # Placeholder for logic to create a review, including
        # validation for user_id, place_id, and rating
        if not is_valid_uuid4(review_data['user_id']):
            raise ValueError('Given user_id is not valid UUID4')
        if not is_valid_uuid4(review_data['place_id']):
            raise ValueError('Given place_id is not valid UUID4')
        exisiting_user = self.user_repo.get(review_data['user_id'])
        if not exisiting_user:
            raise ValueError('No User corresponding to given ID')
        review_data.pop('user_id')
        review_data['user'] = exisiting_user
        existing_place = self.place_repo.get(review_data['place_id'])
        if not existing_place:
            raise ValueError('No Place corresponding to given place '
                             'ID')
        review_data.pop('place_id')
        review_data['place'] = existing_place
        review = Review(**review_data)
        self.review_repo.add(review)
        return review



    def get_review(self, review_id):
        # Placeholder for logic to retrieve a review by ID
        pass

    def get_all_reviews(self):
        # Placeholder for logic to retrieve all reviews
        pass

    def get_reviews_by_place(self, place_id):
        # Placeholder for logic to retrieve all reviews for a specific place
        pass

    def get_review_by_place_and_user(self, place_id, user_id):
        pass

    def update_review(self, review_id, review_data):
        # Placeholder for logic to update a review
        pass

    def delete_review(self, review_id):
        # Placeholder for logic to delete a review
        pass