from app.models.baseEntity import type_validation
from app.services.ressources import is_valid_uuid4
from app.api.v1.apiRessources import validate_init_args
from app.models.place import Place


class PlaceService:
    @classmethod
    def create_place(cls, facade, place_data):
        owner_id = place_data.get('owner_id')
        if not owner_id:
            raise ValueError('Place data does not contain owner_id key')
        type_validation(owner_id, 'owner_id', str)
        if not is_valid_uuid4(owner_id):
            raise ValueError('Invalid owner_id: given owner_id is not '
                             'valid UUID4')
        existing_user = facade.get_user(owner_id)
        if not existing_user:
            raise ValueError('Invalid user: no user corresponding to owner_id')
        place_data.pop('owner_id')
        place_data['owner'] = existing_user
        amenities = place_data.get('amenities_ids')
        if amenities is not None:
            place_data.pop('amenities_ids')
            type_validation(amenities, 'amenities', (str | list))
        validate_init_args(Place, **place_data)
        new_place = Place(**place_data)
        if amenities is not None:
            if isinstance(amenities, list):
                for amenity_id in amenities:
                    type_validation(amenity_id, 'amenity_id', str)
                    if len(amenity_id.strip()) == 0:
                        continue
                    if not is_valid_uuid4(amenity_id):
                        raise ValueError(f"Given amenity_id "
                                         "'{amenity_id}' is not a "
                                         "valid UUID4")
                    current_amenity = facade.get_amenity(amenity_id)
                    if not current_amenity:
                        raise ValueError(f"Amenity with id "
                                         "'{amenity_id}' was not "
                                         "found")
                    new_place.add_amenity(current_amenity)
        # Delete amenities from place_data if they aren't needed for
        # the Place model
        # place_data.pop('amenities', None)
        # Validate the place data
        # new_place = Place(**place_data)
        # Store the new place in the
        # repository
        facade.place_repo.add(new_place)
        return facade.place_repo.get(new_place.id)
