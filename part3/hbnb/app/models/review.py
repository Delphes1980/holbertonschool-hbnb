from app.models.baseEntity import (BaseEntity, type_validation,
                                   strlen_validation)
from app.models.place import Place
from app.models.user import User
from app.api.v1.apiRessources import CustomError

class Review(BaseEntity):
    def __init__(self, text: str, rating: int, place: Place,
                 user: User):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
        if any(review.user == user for review in place.reviews):
            raise CustomError('This user has already reviewed this place',
                              400)
        place.add_review(self)

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text):
        if text is None:
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
        self.__rating = self.rating_validation(rating)

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
        return self.__user

    @user.setter
    def user(self, user):
        self.__user = self.set_user(user)

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
        return self.__place

    @place.setter
    def place(self, place):
        self.__place = self.set_place(place)

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
