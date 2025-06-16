from hbnb.app.models.place import Place
from hbnb.app.models.user import User
from hbnb.app.models.review import Review
from hbnb.app.models.amenity import Amenity

def test_place_creation():
    owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
    place = Place(title="Cozy Apartment", description="A nice place to stay", price=100, latitude=37.7749, longitude=-122.4194, owner=owner)

    # Adding a review
    review = Review(text="Great stay!", rating=5, place=place, user=owner)
    # place.add_review(review)

    assert place.title == "Cozy Apartment"
    assert place.price == 100
    assert len(place.reviews) == 1
    assert place.reviews[0].text == "Great stay!"
    print("Place creation and relationship test passed!")

test_place_creation()


someUser = User("John", "Doe", "example@gmail.com")
print("User was created")
somePlace = Place("Some place", "good place", 30.5, 42.3, 7.5, someUser)
print("Place was created")
someAmenity = Amenity("Wi-Fi")
print("Amenity was created")
somePlace.add_amenity(someAmenity)
print("Amenity was added to Place")
someReview = Review("I liked the place.", 5, somePlace, someUser)
print("Review was created")
somePlace.add_review(someReview)
print("Review was added to Place")

print(someUser.__dict__)
print(somePlace.__dict__)
print(someReview.__dict__)
print(someAmenity.__dict__)
