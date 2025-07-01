from app.models.baseEntity import (BaseEntity, type_validation,
                                   strlen_validation)
from app import db
from sqlalchemy import Column, Integer, String


class Amenity(BaseEntity):
    __tablename__ = 'amenities'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)

    def __init__(self, name):
        super().__init__()
        self.name = name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = self.name_validation(value)

    def name_validation(self, name: str):
        """Verify if the name is a string < 50 characters."""
        type_validation(name, "name", str)
        name = " ".join(name.split())
        strlen_validation(name, "name", 1, 50)
        return name

    # def to_dict(self):
    #     """ Convert the Amenity object to a dictionary representation,
    #     including BaseEntity fields """
    #     base_dict = super().to_dict()
    #     base_dict.update({"name": self.name})
    #     return base_dict
