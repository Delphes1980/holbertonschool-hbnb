from app.models.baseEntity import (BaseEntity, type_validation,
                                   strlen_validation)
from app.models.place import Place
from app.models.user import User
from app import bcrypt, db
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import mapped_column, Mapped
from app.api.v1.apiRessources import CustomError
from sqlalchemy.ext.hybrid import hybrid_property

class Review(BaseEntity):
    __tablename__ = 'reviews'
    # id = db.Column(db.Integer, primary_key=True)
    _text: Mapped[str] = mapped_column("text", Text, nullable=False)
    _rating: Mapped[int] = mapped_column("rating", Integer,
                                         nullable=False)

    def __init__(self, text: str, rating: int, place: Place,
                 user: User):
        super().__init__()
        self.text = text
        # self.rating = self.rating_validation(rating)
        # self.place = self.set_place(place)
        # self.user = self.set_user(user)
        self.rating = rating
        self.place = place
        self.user = user
        if any(review.user == user for review in place.reviews):
            raise CustomError('This user has already reviewed this place',
                              400)
        place.add_review(self)

    @hybrid_property
    def text(self): # type: ignore
        return self._text

    @text.setter # type: ignore
    def text(self, value):
        if value is None:
            raise ValueError("text is required: provide content for"
                             " the review")
        type_validation(value, "Text", str)
        value = value.strip()
        strlen_validation(value, "Text", 2, 500)
        self._text = value

    @hybrid_property
    def rating(self): #type: ignore
        return self._rating

    @rating.setter
    def rating(self, value):
        self._rating = self.rating_validation(value)

    def rating_validation(self, rating):
        if rating is None:
            raise ValueError("rating is required: provide an integer"
                             " between 1 and 5 to rate the place")
        type_validation(rating, "Rating", int)
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and"
                             " 5, both inclusive")
        return rating

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        self._user = self.set_user(value)

    def set_user(self, user):
        if user is None:
            raise ValueError("user is required: provide user who"
                             " writes the review")
        type_validation(user, "User", User)
        if user == self.place.owner:
            raise CustomError("User cannot review their own place", 400)
        return user

    @property
    def place(self):
        return self._place

    @place.setter
    def place(self, value):
        self._place = self.set_place(value)

    def set_place(self, place):
        if place is None:
            raise ValueError("place is required: provide place being"
                             " reviewed")
        type_validation(place, "Place", Place)
        return place

    # def to_dict(self):
    #     return {'id': self.id,
    #             'user_id': self.user.id,
    #             'place_id': self.place.id}
