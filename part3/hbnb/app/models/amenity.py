from app.models.baseEntity import (BaseEntity, type_validation,
                                   strlen_validation)
from app import db
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase, relationship
from typing import Any, List, TYPE_CHECKING
if TYPE_CHECKING:
    from .place import Place


place_amenity = Table(
    "place_amenity", db.metadata,
    Column("place_id", String(36), ForeignKey("places.id"), primary_key=True),
    Column("amenity_id", String(36), ForeignKey("amenities.id"),
           primary_key=True)
    )


class Amenity(BaseEntity):
    __tablename__ = 'amenities'
    # id = db.Column(db.Integer, primary_key=True, nullable=False)
    _name: Mapped[str] = mapped_column("name", String(128), nullable=False,
                                       unique=True)
    # name = db.Column(db.String(128), nullable=False)
    places: Mapped[List["Place"]] = relationship("Place",
                                                 secondary=place_amenity,
                                                 back_populates="_amenities",
                                                 lazy=True)

    def __init__(self, name):
        super().__init__()
        self.name = name

    @hybrid_property
    def name(self) -> Any:  # type: ignore
        # Pylance may warn about 'name' being redefined (or obscured), but
        # this is required for property setters.
        return self._name  # type: ignore

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
