from app.models.place import Place
from app import db
from app.persistence.repository import SQLAlchemyRepository


class PlaceRepository(SQLAlchemyRepository):

    def __init__(self):
        super().__init__(Place)

    def get_place(self, place_id):
        return self.get(place_id)

    def get_all_places(self):
        return self.get_all()

    def create_place(self, place_obj):
        new_place = self.add(place_obj)
        return new_place

    def update_place(self, place_id, place_data):
        return self.update(place_id, place_data)

    def delete_place(self, place_id):
        return self.delete(place_id)
