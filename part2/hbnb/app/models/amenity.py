from hbnb.app.models.baseEntity import BaseEntity


class Amenity(BaseEntity):
    def __init__(self, name):
        self.name = name

    def validate_name(self, name):
        """Verify if the name is a string < 50 characters."""
        max_length = 50
        if not isinstance(name, str):
            raise TypeError("The name of the amenity must be a string")
        if len(name) > max_length:
            raise ValueError(f"Name is more than {max_length} characters.")
        return name
