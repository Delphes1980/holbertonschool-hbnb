from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

# Define the response model for returning place data
place_response_model = api.inherit('PlaceResponse', place_model, {
    'id': fields.String(description='Unique identifier for the place'),
    'created_at': fields.DateTime(dt_format='iso8601', description='Timestamp of creation (ISO 8601)'),
    'updated_at': fields.DateTime(dt_format='iso8601', description='Timestamp of the last update (ISO 8601)')
})

@api.route('/')
class PlaceList(Resource):
    @api.doc('create place')
    @api.marshal_with(place_response_model)
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        # api.payload automatically parses and validates the request JSON against amenity_model
        data = api.payload
        try:
            # Call the facade to create a new place
            new_place = facade.create_place(data)
            # Return the created place as a dictionary
            return new_place.to_dict(), 201
        except ValueError as e:
            api.abort(400, message=str(e))

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
            api.abort(404, 'Place not found')
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
                api.abort(404, 'Place not found')
            return updated_place.to_dict(), 200
        except ValueError as e:
            api.abort(400, message=str(e))
