from hbnb.app.models.baseEntity import BaseEntity
from hbnb.app.models.place import Place
from hbnb.app.models.user import User

class Review(BaseEntity):
    def __init__(self, text: str, rating: int, place: Place,
                 user: User):
        if not text:
            raise ValueError("text is required: provide content for"
                             " the review")
        if not rating:
            raise ValueError("rating is required: provide an integer"
                             " between 1 and 5 to rate the place")
        if not place:
            raise ValueError("place is required: provide place being"
                             " reviewed")
        if not user:
            raise ValueError("user is required: provide user who"
                             " writes the review")
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    def type_validation(self, arg, arg_name, arg_type):
        if not isinstance(arg, arg_type):
            raise TypeError(f"{arg_name} must be a {arg_type}")
        
    def text_validation(self, text: str):
        max_length = 500
        min_length = 2
        if len(text) < 2 or len(text) > max_length:
            raise ValueError(f"text must be max {max_length} and"
                             f" atleast {min_length} characters long")

    def rating_validation(self, rating: int):
        if rating < 1 or rating > 5:
            raise ValueError("rating must be an integer between 1 and"
                             " 5")

    @property
    def text(self):
        return self.__text
    @text.setter
    def text(self, text: str):
        text = text.strip()
        self.type_validation(text, "text", str)
        self.text_validation(text)
        self.__text = text
    
    @property
    def rating(self):
        return self.__rating
    @rating.setter
    def rating(self, rating: int):
        self.type_validation(rating, "rating", int)
        self.rating_validation(rating)
        self.__rating = rating

if __name__ == "__main__":
    somePlace = Place()
    myUser = User("John", "Smith", "john@smith.com")
    review = Review("I liked the place.", 5, somePlace, myUser)
    print(review.__dict__)
    print("Review was successfully created")
