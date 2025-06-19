# HBNB Project - Partie 2 : Services et API RESTful

This part of the HBNB project involves building a complete RESTful API to manage the entities of an accommodation booking system, including users, places, amenities and reviews, using Flask and Flask-RESTX.

## Table of contents
- [Introduction](#introduction)
- [Functionalities](#functionalities)
- [Structure](#structure)
- [Installation](#installation)
- [API Endpoints](#endpoints)
- [Authors](#authors)

### Introduction
This phase of the HBnB project focuses on building the core functionality of the application using Python and Flask. We'll bring the documented architecture to life by implementing the Presentation and Business Logic layers, defining essential classes, methods, and API endpoints.

The goal is to create a functional and scalable foundation for the application. This involves:

- Business Logic Layer: Developing the core models and logic that drive the application's functionality. This includes defining relationships, handling data validation, and managing interactions between different components.
- Presentation Layer: Defining the services and API endpoints using Flask and Flask-RESTx. We'll structure the endpoints logically, ensuring clear paths and parameters for each operation.

### Functionalities
The application can do a number of things, such as:
- User management (create, read, update)
- Amenities management (create, read, update)
- Places management (create, read, update), including association with an owner (user) and amenities.
- Reviews management (create, read, update, delete), associated with a user and a place.
- Validation of input data via Flask-RESTX models.
- Facade layer to orchestrate operations between the API and the persistence layer.

### Structure
```
hbnb/
├── app/
│   ├── __init__.py
│   ├── api/                      # Contains RESTful API definitions (Flask-RESTX)
│   │   ├── __init__.py
│   │   ├── v1/                   # API version 1
│   │       ├── __init__.py
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       ├── amenities.py
│   ├── models/                   # Defining object classes (User, Amenity, Place, Review)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   ├── amenity.py
│   ├── services/                 # Business logic layer / facade
│   │   ├── __init__.py
│   │   ├── facade.py
│   ├── persistence/              # Persistence layer (InMemoryRepository)
│       ├── __init__.py
│       ├── repository.py
├── run.py                        # Flask application entry point
├── config.py
├── requirements.txt
├── README.md

```

### Installation
#### 1. Clone the repository
git clone (https://github.com/Delphes1980/holbertonschool-hbnb/tree/main/)
cd part2/hbnb/

#### 2. Create and activate a virtual environment
```
python3 -m venv venv
```
then
```
source venv/bin/activate
```

#### 3. Install dependencies
```
pip install -r requirements.txt
```

#### 4. Application utilisation
From the root directory of part 2
```
python run.py
```

### API Endpoints
Here's a detailed list of the available API endpoints, their HTTP methods, and expected payloads:

* **Users (`/users`)**
    * `POST /api/v1/users`: Creates a new user.
        * **Payload Ex:** `{"email": "test@example.com", "first_name": "John", "last_name": "Doe"}`
        * **Success Response:** `201 Created`, the user object.
    * `GET /api/v1/users`: Retrieves all users.
    * `GET /api/v1/users/<user_id>`: Retrieves a user by ID.
    * `PUT /api/v1/users/<user_id>`: Updates a user.
        * **Payload Ex:** `{"first_name": "Jane"}`

* **Amenities (`/amenities`)**
    * `POST /api/v1/amenities`: Creates a new amenity.
        * **Payload Ex:** `{"name": "Wi-Fi"}`
    * `GET /api/v1/amenities`: Retrieves all amenities.
    * `GET /api/v1/amenities/<amenity_id>`: Retrieves an amenity by ID.
    * `PUT /api/v1/amenities/<amenity_id>`: Updates an amenity.
        * **Payload Ex:** `{"name": "Pool"}`

* **Places (`/places`)**
    * `POST /api/v1/places`: Creates a new place.
        * **Payload Ex:** `{"title": "Cozy Apartment", "description": "A lovely place...", "price": 100, "latitude": 48.85, "longitude": 2.35, "owner_id": "UUID_USER"}`
        * **Note:** `owner_id` must correspond to an existing user.
    * `GET /api/v1/places`: Retrieves all places.
    * `GET /api/v1/places/<place_id>`: Retrieves a place by ID.
    * `PUT /api/v1/places/<place_id>`: Updates a place.
        * **Payload Ex (to add/modify amenities):** `{"amenities": ["UUID_AMENITY_1", "UUID_AMENITY_2"]}`
        * **Note:** The `amenities` list is an array of UUIDs of existing amenities.

* **Reviews (`/reviews`)**
    * `POST /api/v1/places/<place_id>/reviews`: Creates a review for a specific place.
        * **Payload Ex:** `{"user_id": "UUID_USER", "text": "Very pleasant stay.", "rating": 5}`
        * **Note:** `user_id` must be an existing user.
    * `GET /api/v1/places/<place_id>/reviews`: Retrieves reviews for a specific place.
    * `GET /api/v1/users/<user_id>/reviews`: Retrieves reviews by a specific user.
    * `GET /api/v1/reviews/<review_id>`: Retrieves a review by ID.
    * `PUT /api/v1/reviews/<review_id>`: Updates a review.
        * **Payload Ex:** `{"rating": 4}`
    * `DELETE /api/v1/reviews/<review_id>`: Deletes a review.

### Authors
- [Delphine Coutouly-Laborda](https://github.com/Delphes1980)
- [Xavier Laforgue](https://github.com/XavierLaforgue)