from hbnb.app.models.place import Place
from hbnb.app.models.user import User
from hbnb.app.models.review import Review
from hbnb.app.models.amenity import Amenity


someUser = User("John", "Smith", "john@smith.com")
print("User was created")
print(someUser.__dict__)
somePlace = Place("Apartment somewehere",
                    "Nice place near a beach.", 30.5, 43,
                    7.01667, someUser)
print("Place was created:")
print(somePlace.__dict__)
someReview = Review("I liked the place.", 5, somePlace, someUser)
print("Review was created and added to Place")
print(someReview.__dict__)
print("Updated Place with Review:")
print(somePlace.__dict__)
