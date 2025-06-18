# Business Logic Layer

The Business Logic Layer is responsible for handling the core rules and operations of the application. It is composed of several main entities:

## Entities and Responsibilities

- **User**  
  Represents a user of the platform.  
  Responsibilities: creation, authentication, and management of personal information.

- **Place**  
  Represents a property or listing.  
  Responsibilities: creation, update, validation of attributes (title, price, location), owner management, association with amenities and reviews.

- **Amenity**  
  Represents a facility or service available in a property.  
  Responsibilities: management of the list of amenities.

- **Review**  
  Represents a review left by a user on a property.  
  Responsibilities: creation, content validation, association with a user and a property.

## Usage Examples

### Creating a User
```python
from app.models.user import User

user = User(first_name="Alice", last_name="Smith", email="alice@email.com", password="securepwd")
```

### Creating a Place
```python
from app.models.place import Place

place = Place(
    title="Cozy Studio",
    description="Studio in the city center",
    price=80,
    latitude=48.8566,
    longitude=2.3522,
    owner=user.id
)
```

### Adding an Amenity to a Place
```python
from app.models.amenity import Amenity

wifi = Amenity(name="WiFi")
place.add_amenity(wifi)
```

### Checking Ownership
```python
place.is_owner(user.id)  # Returns True if the user is the owner
```

### Adding a Review
```python
from app.models.review import Review

review = Review(content="Great stay!", user_id=user.id, place_id=place.id)
place.add_review(review)
```
