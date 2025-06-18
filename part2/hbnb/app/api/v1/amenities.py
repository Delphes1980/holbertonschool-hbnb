from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

# Define the response model for returning amenity data
amenity_response_model = api.inherit('AmenityResponse', amenity_model, {
    'id': fields.String(description='Unique identifier for the amenity'),
    'created_at': fields.DateTime(dt_format='iso8601', description='Timestamp of creation (ISO 8601)'),
    'updated_at': fields.DateTime(dt_format='iso8601', description='Timestamp of the last update (ISO 8601)')
})


@api.route('/')
class AmenityList(Resource):
    @api.doc('create_amenity')
    @api.expect(amenity_model, validate=True)
    @api.marshal_with(amenity_response_model)
    @api.response(201, 'Amenity successfully created', amenity_response_model)
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        # api.payload automatically parses and validates the request JSON against amenity_model
        data = api.payload
        try:
            # Call the facade to create a new amenity
            new_amenity = facade.create_amenity(data)
            # Return the created amenity as a dictionary
            return new_amenity.to_dict(), 201
        except ValueError as e:
            api.abort(400, message=str(e))

    @api.doc('list_amenities')
    @api.marshal_list_with(amenity_response_model)
    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        # Call the facade to get all amenities
        amenities = facade.get_all_amenities()
        # Convert each amenity to a dictionary & return the list
        return [amenity.to_dict() for amenity in amenities], 200


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.doc('get_amenity_by_id')
    @api.marshal_with(amenity_response_model)
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        # Call the facade to retrieve an amenity by ID
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, 'Amenity not found')
        return amenity.to_dict(), 200

    @api.doc('update_amenity')
    @api.expect(amenity_model)
    @api.marshal_with(amenity_response_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        # api.payload automatically parses and validates the request JSON against amenity_model
        new_amenity_data = api.payload
        try:
            updated_amenity = facade.update_amenity(amenity_id, new_amenity_data)
            # If the amenity is not found, return an error
            # Otherwise, return the updated amenity as a dictionary
            if not updated_amenity:
                api.abort(404, 'Amenity not found')
            return updated_amenity.to_dict(), 200
        except (TypeError, ValueError):
            api.abort(400, 'Invalid input data')
