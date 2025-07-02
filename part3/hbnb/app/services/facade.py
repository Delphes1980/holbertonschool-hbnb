from app.persistence.repository import InMemoryRepository
from app.services.PlaceService import PlaceService
from app.services.UserService import UserService
from app.services.AmenityService import AmenityService
from app.models.review import Review
from app.models.baseEntity import type_validation
from app.services.ressources import is_valid_uuid4

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

# Services for User CRUD operations ####

    def create_user(self, user_data):
        """Create a new user with the provided data."""
        return UserService.create_user(self, user_data)

    def get_user(self, user_id):
        """Retrieve a user by their ID."""
        return UserService.get_user(self, user_id)

    def get_all_users(self):
        """Retrieve all users from the repository."""
        return self.user_repo.get_all()

    def get_user_by_email(self, email):
        """Retrieve a user by their email address."""
        return UserService.get_user_by_email(self, email)

    def update_user(self, user_id, user_data):
        """Update an existing user's data."""
        return UserService.update_user(self, user_id, user_data)

# Services for Amenity CRUD operations ########

    def create_amenity(self, amenity_data):
        """Create a new amenity with the provided data."""
        return AmenityService.create_amenity(self, amenity_data)

    def get_amenity(self, amenity_id):
        """ Retrieve an amenity by its ID """
        return AmenityService.get_amenity(self, amenity_id)

    def get_all_amenities(self):
        """ Retrieve all amenities """
        return self.amenity_repo.get_all()

    def get_amenity_by_name(self, name):
        return AmenityService.get_amenity_by_name(self, name)

    def update_amenity(self, amenity_id, amenity_data):
        """ Update an amenity with the provided data """
        return AmenityService.update_amenity(self, amenity_id,
                                             amenity_data)

# Services for Place CRUD operations ########

    def create_place(self, place_data):
        """ Create a new place with the provided data """
        return PlaceService.create_place(self, place_data)

    def get_place(self, place_id):
        """ Retrieve a place by its ID """
        if not is_valid_uuid4(place_id):
            raise ValueError('Given place_id is not valid UUID4')
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """ Retrieve all places """
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """ Update a place with the provided data """
        place = self.get_place(place_id)
        if not place:
            return None
        owner_id = place_data.get('owner_id')
        if not owner_id:
            raise ValueError('Place data does not contain owner_id key')
        type_validation(owner_id, 'owner_id', str)
        if not is_valid_uuid4(owner_id):
            raise ValueError('Given owner_id is not valid UUID4')
        existing_user = self.get_user(owner_id)
        if not existing_user:
            raise ValueError('No User corresponding to owner_id')
        place_data.pop('owner_id')
        place_data['owner'] = existing_user
        amenities_ids = place_data.get('amenities')
        if amenities_ids:
            place_data.pop('amenities')
            amenities = []
            for amenity_id in amenities_ids:
                if not is_valid_uuid4(amenity_id):
                    raise ValueError(f"Given amenity_id={amenity_id} "
                                     "is not a valid UUID4")
                amenities.append(self.get_amenity(amenity_id))
            place_data['amenities'] = amenities
        place.update(place_data)
        # updated_place = self.place_repo.get(place_id)
        return place

# Services for Review CRUD operations ########

    def create_review(self, review_data):
        # Placeholder for logic to create a review, including
        # validation for user_id, place_id, and rating
        user_id = review_data.get('user_id')
        if not user_id:
            raise ValueError('Review data does not contain user_id key')
        type_validation(user_id, 'user_id', str)
        if not is_valid_uuid4(user_id):
            raise ValueError('Given user_id is not valid UUID4')
        place_id = review_data.get('place_id')
        if not place_id:
            raise ValueError('Review data does not contain place_id key')
        if not is_valid_uuid4(place_id):
            raise ValueError('Given place_id is not valid UUID4')
        exisiting_user = self.user_repo.get(user_id)
        if not exisiting_user:
            raise ValueError('No User corresponding to given ID')
        existing_place = self.place_repo.get(place_id)
        if not existing_place:
            raise ValueError('No Place corresponding to given place '
                             'ID')
        if self.get_review_by_place_and_user(place_id, user_id):
            raise ValueError(
                'User already left a review for this place')
        review_data.pop('user_id')
        review_data['user'] = exisiting_user
        review_data.pop('place_id')
        review_data['place'] = existing_place
        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        if not is_valid_uuid4(review_id):
            raise ValueError('Given review_id is not valid UUID4')
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        if not is_valid_uuid4(place_id):
            raise ValueError('Given place_id is not valid UUID4')
        place = self.get_place(place_id)
        if not place:
            return None
        return place.reviews

    def get_review_by_place_and_user(self, place_id, user_id):
        reviews = self.get_reviews_by_place(place_id)
        if not reviews:
            return None
        for review in reviews:
            if review.user.id == user_id:
                return review
        return None

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if not review:
            return None
        # self.review_repo.update(review_id, review_data)
        review.update(review_data)
        return review

    def delete_review(self, review_id):
        review = self.get_review(review_id)
        if not review:
            raise ValueError('Review not found')
        for review_in_place in review.place.reviews:
            if review_in_place.id == review.id:
                review.place.reviews.remove(review)
        self.review_repo.delete(review_id)
        del review
