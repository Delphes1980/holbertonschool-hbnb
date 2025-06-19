from flask_restx import Namespace, Resource, fields, _http
from app.services import facade

api = Namespace('places', description='Place operations')

amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(required=True, description='Amenity ID'),
    'name': fields.String(required=True,
                          description='Name of the amenity')
})

user_model = api.model('PlaceOwner', {
    'id': fields.String(required=True, description='Owner ID'),
    'first_name': fields.String(required=True, 
                                description='First name of the owner'),
    'last_name': fields.String(required=True, 
                               description='Last name of the owner'),
    'email': fields.String(required=True, 
                           description='Email of the owner')
})

review_model = api.model('PlaceReview', {
    'id': fields.String(required=True, description='Review ID'),
    'text': fields.String(required=True,
                          description='Text of the review'),
    'rating': fields.Integer(required=True, 
                             description='Rating of the place (1-5)'),
    'user_id': fields.String(
        required=True,
        description='ID of the user who left the review')
})

place_model = api.model('Place', {
    'title': fields.String(required=True,
                           description='Title of the place'),
    'description': fields.String(
        required=False,
        description='Description of the place'),
    'price': fields.Float(required=True,
                          description='Price per night'),
    'latitude': fields.Float(required=True,
                             description='Latitude of the place'),
    'longitude': fields.Float(required=True,
                              description='Longitude of the place'),
    'owner_id': fields.String(required=True,
                              description='ID of the owner'),
    'amenities': fields.List(fields.String,
                             required=True,
                             description="List of amenities ID's")
})
place_response_model = api.model('PlaceResponse', {
    'id': fields.String(required=True, 
                        description='Unique identifier for the place'),
    'title': fields.String(required=True,
                           description='Title of the place'),
    'description': fields.String(
        required=False, 
        description='Description of the place'),
    'price': fields.Float(required=True,
                          description='Price per night'),
    'latitude': fields.Float(required=True,
                             description='Latitude of the place'),
    'longitude': fields.Float(required=True,
                              description='Longitude of the place'),
    'owner': fields.Nested(user_model, required=True,
                           description='Owner of the place'),
    'amenities': fields.List(fields.Nested(amenity_model),
                             required=True,
                             description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model),
                           required=True,
                           description='List of reviews')
})

# place_response_model = api.inherit('PlaceResponse', place_model, {
#     'id': fields.String(description='Unique identifier for the place'),
#     'created_at': fields.DateTime(dt_format='iso8601', description='Timestamp of creation (ISO 8601)'),
#     'updated_at': fields.DateTime(dt_format='iso8601', description='Timestamp of the last update (ISO 8601)')
# })

@api.route('/')
class PlaceList(Resource):
    @api.doc('Returned the created place')
    @api.marshal_with(place_response_model,
                      code=_http.HTTPStatus.CREATED,
                      description='Place successfully created')
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        place_data = api.payload
        try:
            place = facade.create_place(place_data)
        except Exception as e:
            api.abort(400, error=str(e))
            return {'error': str(e)}, 400
        return place, 201

    @api.doc('list_places')
    @api.marshal_list_with(place_response_model)
    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        # Call the facade to get all places
        places = facade.get_all_places()
        # Convert each place to a dictionary & return the list
        return [place.to_dict() for place in places], 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.doc('get_place_by_id')
    @api.marshal_with(place_response_model)
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        # Call the facade to retrieve a place by ID
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, error='Place not found')
        return place.to_dict(), 200

    @api.doc('update_place')
    @api.expect(place_model)
    @api.marshal_with(place_response_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        # api.payload automatically parses and validates the request JSON against amenity_model
        new_place_data = api.payload
        try:
            updated_place = facade.update_place(place_id, new_place_data)
            # If the place is not found, return an error
            # Otherwise, return the updated place as a dictionary
            if not updated_place:
                api.abort(404, error='Place not found')
                return {'returned error': 
                        'returned Place not found'}, 404
            return updated_place.to_dict(), 200
        except ValueError as e:
            api.abort(400, message=str(e))

@api.route('/<place_id>/reviews')
class PlaceReviewsList(Resource):
    @api.doc('Returns list of reviews given to the selected place')
    @api.response(200, 'List of reviews retrieved successfully')
    @api.response(404, 'Place not found')
    @api.response(400, "Invalid ID")
    def get(self, place_id):
        """Get list of reviews for a place given its ID"""
        if not is_valid_uuid4(place_id):
            return {'error': 'Invalid UUID: provided ID is not a valid'
                             ' UUID4'}, 400
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        place.reviews
        return [{"id": review.id,
                 "rating": review.rating,
                 "text": review.text,
                 "place_id": review.place.id,
                 "user_id": review.user.id
                 } for review in place.reviews], 200
