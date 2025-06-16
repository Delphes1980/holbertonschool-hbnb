from hbnb.app.models.baseEntity import BaseEntity, type_validation
from hbnb.app.models.user import User


class Place(BaseEntity):
    def __init__(self, title, description, price, latitude,
                 longitude, owner):
        super().__init__()
        self.title = self.validate_title(title)
        self.description = self.validate_description(description)
        self.price = self.validate_price(price)
        self.latitude = self.validate_latitude(latitude)
        self.longitude = self.validate_longitude(longitude)
        self.owner = self.validate_owner(owner)
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities

    def add_review(self, review):
        """Add a review to the place."""
        from hbnb.app.models.review import Review
        type_validation(review, "Review", Review)
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        from hbnb.app.models.amenity import Amenity
        type_validation(amenity, "Amenity", Amenity)
        self.amenities.append(amenity)

    def validate_title(self, title):
        """Verify if the title is a string < 100 characters."""
        max_length = 50
        min_length = 4
        type_validation(title, "Title", str)
        title = title.strip()
        if len(title) > max_length or len(title) < min_length:
            raise ValueError(f"title cannot exceed {max_length}"
                             f" characters nor have fewer than"
                             f" {min_length}")
        return title

    def validate_description(self, description):
        """Verify if the description is a string."""
        max_length = 50
        min_length = 4
        type_validation(description, "Description", str)
        description = description.strip()
        if (len(description) > max_length or
                len(description) < min_length):
            raise ValueError(f"description cannot exceed {max_length}"
                             f" characters nor have fewer than"
                             f" {min_length} characters")
        return description

    def validate_price(self, price: float):
        """Verify is the price is an integer."""
        type_validation(price, "price", (float, int))
        if price < 0:
            raise ValueError("price must be a positive number")
        return float(price)

    def validate_latitude(self, latitude):
        """Verify is the latitude is a float between -90.0 & 90.0."""
        if not isinstance(latitude, float | int):
            raise TypeError("Latitude must be a number")
        if not (-90.0 <= latitude <= 90.0):
            raise ValueError("Latitude must be between -90.0 and 90.0.")
        return float(latitude)

    def validate_longitude(self, longitude):
        """Verify is the longitude is a float between -180.0 & 180.0."""
        if not isinstance(longitude, float | int):
            raise TypeError("Longitude must be a number")
        if not (-180.0 <= longitude <= 180.0):
            raise ValueError("Longitude must be between -180.0 and"
                             " 180.0")
        return float(longitude)

    def validate_owner(self, owner):
        if not isinstance(owner, User):
            raise TypeError("owner is not a User")
        return owner

    def is_owner(self, owner, User_id):
        """Verify is the user owns the place."""
        if owner.id != User_id:
            raise ValueError("Unauthorized access: the current user "
                             "is not the owner")
        return True
