from app.models.baseEntity import (BaseEntity, type_validation,
                                        strlen_validation)
from app.models.user import User


class Place(BaseEntity):
    def __init__(self, title:str, description=None, price:float=-1,
                 latitude:float=-360, longitude:float=-360, owner=None):
        super().__init__()
        self.title = self.validate_title(title)
        self.description = self.validate_description(description)
        self.price = self.validate_price(price)
        self.latitude = self.validate_latitude(latitude)
        self.longitude = self.validate_longitude(longitude)
        self.owner = owner
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities

    def add_review(self, review):
        """Add a review to the place."""
        from app.models.review import Review
        type_validation(review, "Review", Review)
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        from app.models.amenity import Amenity
        type_validation(amenity, "Amenity", Amenity)
        self.amenities.append(amenity)

    def validate_title(self, title):
        """Verify if the title is a string < 100 characters."""
        if not title:
            raise ValueError("Title is required")
        type_validation(title, "Title", str)
        title = title.strip()
        strlen_validation(title, "Title", 4, 100)
        return title

    def validate_description(self, description):
        """Verify if the description is a string."""
        if description is None:
            return ""
        type_validation(description, "Description", str)
        description = description.strip()
        strlen_validation(description, "Description", 0, 50)
        return description

    def validate_price(self, price: float):
        """Verify is the price is an integer."""
        type_validation(price, "Price", (float, int))
        if price <= 0:
            raise ValueError("Price must be a positive number (larger "
                             "than 0)")
        return float(price)

    def validate_latitude(self, latitude):
        """Verify is the latitude is a float between -90.0 & 90.0."""
        type_validation(latitude, "Latitude", (float, int))
        if not (-90.0 <= latitude <= 90.0):
            raise ValueError("Latitude must be between -90.0 and 90.0.")
        return float(latitude)

    def validate_longitude(self, longitude):
        """Verify is the longitude is a float between -180.0 & 180.0."""
        type_validation(longitude, "Longitude", (float, int))
        if not (-180.0 <= longitude <= 180.0):
            raise ValueError("Longitude must be between -180.0 and"
                             " 180.0")
        return float(longitude)

    # def is_owner(self, user_id):
    #     """Verify is the user owns the place."""
    #     if self.owner != user_id:
    #         raise PermissionError("Unauthorized access: the current user "
    #                           "is not the owner")
    #     return True

    # def to_dict(self):
    #     """ Convert the Place object to a dictionary representation,
    #     including BaseEntity fields """
    #     base_dict = super().to_dict()
    #     base_dict.update({
    #         "title": self.title,
    #         "description": self.description,
    #         "price": self.price,
    #         "latitude": self.latitude,
    #         "longitude": self.longitude,
    #         "owner_id": self.owner_id,
    #         "reviews": list(self.reviews),
    #         "amenities": list(self.amenities)
    #         })
    #     return base_dict