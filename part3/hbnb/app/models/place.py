from app.models.baseEntity import (BaseEntity, type_validation,
                                   strlen_validation)
from app.models.user import User
from app import db
from sqlalchemy import Column, Integer, String
from app.api.v1.apiRessources import CustomError


class Place(BaseEntity):
    __tablename__ = 'places'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    def __init__(self, title: str, description = None, *,
                 price: float, latitude: float,
                 longitude: float, owner: User):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []  # List to store related reviews
        self.__amenities = []  # List to store related amenities

    def add_review(self, review):
        """Add a review to the place."""
        if review is None:
            raise ValueError('Expected review but received None')
        from app.models.review import Review
        type_validation(review, "Review", Review)
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(self.amenity_validation(amenity))

    def amenity_validation(self, amenity):
        if amenity is None:
            raise ValueError('Invalid amenity: expected amenity but received None')
        from app.models.amenity import Amenity
        type_validation(amenity, "Amenity", Amenity)
        if any(place_amenity == amenity 
               for place_amenity in self.amenities):
            raise CustomError(f'Amenity "{amenity.name}" already listed for this place', 400)
        return amenity

    @property
    def amenities(self):
        return self.__amenities
    
    @amenities.setter
    def amenities(self, amenities):
        if amenities is None:
            self.__amenities = []
            return None
        type_validation(amenities, "amenities", list)
        for amenity in amenities:
            self.add_amenity(amenity)
            # self.__amenities.append(self.amenity_validation(amenity))

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        self.__title = self.validate_title(value)

    def validate_title(self, title):
        """Verify if the title is a string < 100 characters."""
        if title is None:
            raise ValueError('Invalid title: expected a title but received None')
        type_validation(title, "Title", str)
        title = title.strip()
        strlen_validation(title, "Title", 4, 100)
        return title

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        self.__description = self.validate_description(value)

    def validate_description(self, description):
        """Verify if the description is a string."""
        if description is None:
            return None # ""
        type_validation(description, "Description", str)
        description = description.strip()
        strlen_validation(description, "Description", 3, 50)
        return description

    @property
    def price(self):
        return self.price_

    @price.setter
    def price(self, value):
        self.price_ = self.validate_price(value)

    def validate_price(self, price: float):
        """Verify is the price is an integer."""
        if price is None:
            raise ValueError("Invalid price: expected float or int but received None")
        type_validation(price, "Price", (float, int))
        if price <= 0:
            raise ValueError("Price must be a positive number (larger "
                             "than 0)")
        return float(price)

    @property
    def latitude(self):
        return self.__latitude

    @latitude.setter
    def latitude(self, value):
        self.__latitude = self.validate_latitude(value)

    def validate_latitude(self, latitude):
        """Verify is the latitude is a float between -90.0 & 90.0."""
        if latitude is None:
            raise ValueError("Invalid latitude: expected float or int but received None")
        type_validation(latitude, "Latitude", (float, int))
        if not (-90.0 <= latitude <= 90.0):
            raise ValueError("Latitude must be between -90.0 and 90.0.")
        return float(latitude)

    @property
    def longitude(self):
        return self.__longitude

    @longitude.setter
    def longitude(self, value):
        self.__longitude = self.validate_longitude(value)

    def validate_longitude(self, longitude):
        """Verify is the longitude is a float between -180.0 &
        180.0."""
        if longitude is None:
            raise ValueError("Invalid longitude: expected float or int but received None")
        type_validation(longitude, "Longitude", (float, int))
        if not (-180.0 <= longitude <= 180.0):
            raise ValueError("Longitude must be between -180.0 and"
                             " 180.0")
        return float(longitude)

    @property
    def owner(self):
        return self.__owner

    @owner.setter
    def owner(self, value):
        if value is None:
            raise ValueError("Invalid owner: expected user but received None")
        type_validation(value, "owner", User)
        self.__owner = value

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
