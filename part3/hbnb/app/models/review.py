from app.models.baseEntity import (BaseEntity, type_validation,
                                   strlen_validation)
from app.models.place import Place
from app.models.user import User
from app import bcrypt, db
from sqlalchemy import Column, Integer, String


class Review(BaseEntity):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = self.set_place(place)
        self.user = self.set_user(user)
        place.add_review(self)

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text):
        if not text:
            raise ValueError("text is required: provide content for"
                             " the review")
        type_validation(text, "Text", str)
        text = text.strip()
        strlen_validation(text, "Text", 2, 500)
        self.__text = text

    @property
    def rating(self):
        return self.__rating

    @rating.setter
    def rating(self, rating):
        if not rating:
            raise ValueError("rating is required: provide an integer"
                             " between 1 and 5 to rate the place")
        type_validation(rating, "Rating", int)
        self.rating_validation(rating)
        self.__rating = rating

    def rating_validation(self, rating):
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and"
                             " 5, both inclusive")

    def set_user(self, user):
        if not user:
            raise ValueError("user is required: provide user who"
                             " writes the review")
        type_validation(user, "User", User)
        return user

    def set_place(self, place):
        if not place:
            raise ValueError("place is required: provide place being"
                             " reviewed")
        type_validation(place, "Place", Place)
        return place

    # def to_dict(self):
    #     return {'id': self.id,
    #             'user_id': self.user.id,
    #             'place_id': self.place.id}
