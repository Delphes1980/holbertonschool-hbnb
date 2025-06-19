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

    def create_place(self, place_data):
        """ Create a new place with the provided data """
        # Check if the owner exists
        if 'owner_id' not in place_data:
            raise ValueError("Owner Id is required")
        
        owner_id = place_data['owner_id']
        owner_obj = self.user_repo.get(owner_id)
        if not owner_obj:
            raise ValueError(f"Owner with ID '{owner_id}' does not exist")
        amenity_ids_from_payload = place_data.pop('amenities', [])
        place_init_data = {
            "title": place_data.get('title'),
            "description": place_data.get('description'),
            "price": place_data.get('price'),
            "latitude": place_data.get('latitude'),
            "longitude": place_data.get('longitude'),
            "owner": owner_obj.id
        }
        new_place = Place(**place_init_data)
        for amenity_id in amenity_ids_from_payload:
            amenity_obj = self.amenity_repo.get(amenity_id)
            if amenity_obj:
                new_place.add_amenity(amenity_obj)
            else:
                print(f"Amenity with ID '{amenity_id}' not found and skipped for Place creation")
        self.place_repo.add(new_place)
        return new_place


    def get_place(self, place_id):
        """ Retrieve a place by its ID """
        place = self.place_repo.get(place_id)
        if not place:
            return None
        owner_id_from_place = place.owner
        place.owner = self.user_repo.get(owner_id_from_place)
        amenities = []
        for amenity_id in place.amenities:
            amenity_obj = self.amenity_repo.get(amenity_id)
            if amenity_obj:
                amenities.append(amenity_obj)
        place.amenities = amenities
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
        if 'owner_id' in place_data:
            new_owner_id = place_data['owner_id']
            new_owner_obj = self.user_repo.get(new_owner_id)
            if not new_owner_obj:
                raise ValueError("New owner does not exist")
            place_to_update.owner = new_owner_obj.id
            place_data.pop('owner_id')
        amenity_ids_to_add = place_data.pop('amenities', None)
        updated_place = self.place_repo.get(place_id)
        if amenity_ids_to_add is not None:
            updated_place.amenities = []
        for amenity_id in amenity_ids_to_add:
            amenity_obj = self.amenity_repo.get(amenity_id)
            if amenity_obj:
                updated_place.add_amenity(amenity_obj)
            else:
                print("Amenity not found")

        return self.get_place(place_id)

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
