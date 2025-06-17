from hbnb.app.models.baseEntity import (BaseEntity, type_validation,
                                        strlen_validation)


class Amenity(BaseEntity):
    def __init__(self, name):
        super().__init__()
        if not name:
            raise ValueError("Name of the Amenity is required")
        self.name = self.set_name(name)

    def set_name(self, name):
        """Verify if the name is a string < 50 characters."""
        type_validation(name, "Name of the Amenity", str)
        name = name.strip()
        strlen_validation(name, "Name of the Amenity", 1, 50)
        return name
