from app.models.baseEntity import (BaseEntity, type_validation,
                                   strlen_validation)


class Amenity(BaseEntity):
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
