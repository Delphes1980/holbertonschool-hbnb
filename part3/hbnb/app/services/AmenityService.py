from app.models.amenity import Amenity
from app.services.ressources import is_valid_uuid4
from app.api.v1.apiRessources import validate_init_args    
from app.models.baseEntity import type_validation

class AmenityService:

    @classmethod
    def create_amenity(cls, facade, amenity_data):
        """Create a new amenity with the provided data."""
        name = amenity_data.get('name')
        type_validation(name, 'name', str)
        if name is None:
            raise ValueError('Invalid name: name is required')
        name = name.strip()
        all_existing_amenities = cls.get_all_amenities(facade)
        for existing_amenity in all_existing_amenities:
            if existing_amenity.name.casefold() == name.casefold():
                raise ValueError('Invalid name: name already registered')
        # existing_amenity = cls.get_amenity_by_name(facade, name)
        # if existing_amenity is not None:
        #     raise ValueError('Invalid name: name already registered')
        validate_init_args(Amenity, **amenity_data)
        new_amenity = Amenity(**amenity_data)
        facade.amenity_repo.add(new_amenity)
        return facade.amenity_repo.get(new_amenity.id)

    @classmethod
    def get_amenity(cls, facade, amenity_id):
        """ Retrieve an amenity by its ID """
        type_validation(amenity_id, 'amenity_id', str)
        if not is_valid_uuid4(amenity_id):
            raise ValueError('Invalid ID: amenity_id is not a valid '
                             'UUID4')
        return facade.amenity_repo.get(amenity_id)

    @classmethod
    def get_all_amenities(cls, facade):
        """ Retrieve all amenities """
        return facade.amenity_repo.get_all()

    @classmethod
    def get_amenity_by_name(cls, facade, name):
        if name is None or (isinstance(name, str) and
                            len(name.strip()) == 0):
            raise ValueError('Invalid name: name is required')
        type_validation(name, 'name', str)
        return facade.amenity_repo.get_by_attribute('name', name)

    @classmethod
    def update_amenity(cls, facade, amenity_id, amenity_data):
        """ Update an amenity with the provided data """
        type_validation(amenity_id, 'amenity_id', str)
        amenity = cls.get_amenity(facade, amenity_id)
        if amenity is None:
            return None
        amenity_by_name = cls.get_amenity_by_name(
                facade,
                amenity_data.get('name'))
        if amenity_by_name and amenity_by_name.id != amenity.id:
            raise ValueError('Invalid name: name is already used for '
                             'another amenity')
        validate_init_args(Amenity, **amenity_data)
        # amenity.update(amenity_data)
        facade.amenity_repo.update(amenity_id, amenity_data)
        updated_amenity = facade.amenity_repo.get(amenity_id)
        return updated_amenity
