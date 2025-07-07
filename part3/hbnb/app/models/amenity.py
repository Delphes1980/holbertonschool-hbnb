from app.models.baseEntity import (BaseEntity, type_validation,
                                   strlen_validation)
from app import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import mapped_column, Mapped
from typing import Any


class Amenity(BaseEntity):
    __tablename__ = 'amenities'
    # id = db.Column(db.Integer, primary_key=True, nullable=False)
    _name: Mapped[str] = mapped_column("name", 
                                       String(128), nullable=False, unique=True)
    # name = db.Column(db.String(128), nullable=False)

    def __init__(self, name):
        super().__init__()
        self.name = name

    @hybrid_property
    def name(self) -> Any: # type: ignore
        # Pylance may warn about 'name' being redefined (or obscured), but this is required for property setters.
        return self._name # type: ignore

    @name.setter 
    def name(self, value: str):
        self._name = self.name_validation(value)

    def name_validation(self, name: str):
        """Verify if the name is a string < 50 characters."""
        if name is None:
            raise ValueError('Invalid name: expected name but received None')
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
