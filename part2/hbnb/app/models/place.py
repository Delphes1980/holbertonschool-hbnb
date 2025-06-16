from hbnb.app.models.baseEntity import BaseModel


class Place(BaseModel):
    def __init__(self, title, description, price, latitude,
                 longitude, owner_id):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

    def validate_title(title):
        """Verify if the title is a string < 100 characters."""
        max_length = 100
        if not isinstance(title, str):
            raise TypeError("Title must be a string")
        if title > max_length:
            raise ValueError(f"Title cannot exceed {max_length} characters")

    def validate_description(description):
        """Verify is the description is a string."""
        if not isinstance(description, str):
            raise TypeError("Description must be a string")
        return description

    def validate_price(price):
        """Verify is the price is an integer."""
        if not isinstance(price, float):
            raise TypeError("Price must be an integer")
        return price

    def validate_latitude(latitude):
        """Verify is the latitude is a float between -90.0 & 90.0."""
        if not isinstance(latitude, float):
            raise TypeError("Latitude must be a number")
        if not (-90.0 <= latitude <= 90.0):
            raise ValueError("Latitude must be between -90.0 and 90.0.")
        return latitude

    def validate_longitude(longitude):
        """Verify is the longitude is a float between -180.0 & 180.0."""
        if not isinstance(longitude, float):
            raise TypeError("Longitude must be a number")
        if not (-180.0 <= longitude <= 180.0):
            raise ValueError("Longitude must be between -180.0 and 180.0")
        return longitude

    def validate_owner(owner_id, User_id):
        """Verify is the user owns the place."""
        if owner_id != User_id:
            raise ValueError("Unauthorized access: the current user "
                             "is not the owner")
        return True
