
from flask_restx import Namespace, Resource, fields
from hbnb.app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

amenity_response_model = api.inherits('AmenityResponse', amenity_model {
    'id': fields.String(description='Unique identifier for the amenity'),
    'created_at': fields.Datetime(dt=format='iso8601', description='Timestamp'
                                  'of creation (ISO 8601)'),
    'updated_at': fields.Datetime(dt=format='iso8601', description='Timestamp'
                                  'of the last update (ISO 8601)')
})


@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model, required=True)
    @api.marshal_with(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        # Placeholder for the logic to register a new amenity
        amenity_name = api.payload.get('name')
        new_amenity = facade.create_amenity(amenity_name)
        return new_amenity.to_dict()

    @api.marshal_list_with(amenity_model)
    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        # Placeholder for logic to return a list of all amenities
        return facade.get_all_amenities()


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.marshal_with(amenity_model)
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        # Placeholder for the logic to retrieve an amenity by ID
        amenity = facade.get_amenity(amenity_id)
        return amenity

    @api.expect(amenity_model)
    @api.marshal_with(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        # Placeholder for the logic to update an amenity by ID
        updated_id = api.payload['amenity_id']
        new_amenity_data = api.payload
        return facade.update_amenity(amenity_id, new_amenity_data)
