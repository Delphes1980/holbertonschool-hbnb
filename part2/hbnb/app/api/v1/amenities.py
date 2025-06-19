from flask_restx import Namespace, Resource, fields, _http
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

amenity_response_model = api.model('AmenityResponse', {
    'id': fields.String(
        required=True,
        description='Unique identifier for the amenity'),
    'name': fields.String(required=True,
                          description='Name of the amenity')
})

# Define the response model for returning amenity data
# amenity_response_model = api.inherit('AmenityResponse', amenity_model, {
#     'id': fields.String(
#         required=True,
#         description='Unique identifier for the amenity'),
    # 'created_at': fields.DateTime(dt_format='iso8601', description='Timestamp of creation (ISO 8601)'),
    # 'updated_at': fields.DateTime(dt_format='iso8601', description='Timestamp of the last update (ISO 8601)')
# })

@api.route('/')
class AmenityList(Resource):
    @api.doc('Returns the created amenity')
    @api.marshal_with(amenity_response_model,
                      code=_http.HTTPStatus.CREATED,
                      description='Amenity successfully created')
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created',
                  amenity_response_model)
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        # api.payload automatically parses and validates the request JSON against amenity_model
        data = api.payload
        try:
            new_amenity = facade.create_amenity(data)
        except ValueError as e:
            api.abort(400, error=str(e))
            return {'error': str(e)}, 400
        return new_amenity, 201

    @api.doc('Returns a list of all registered amenities')
    @api.marshal_list_with(
        amenity_response_model,
        code=_http.HTTPStatus.OK,
        description='List of amenities retrieved successfully')
    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        return facade.get_all_amenities(), 200
        # amenities = facade.get_all_amenities()
        # return [amenity.to_dict() for amenity in amenities], 200

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.doc('Returns amenity corresponding to given ID')
    @api.marshal_with(
        amenity_response_model,
        code=_http.HTTPStatus.OK,
        description='Amenity details retrieved successfully')
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(400, 'Invalid ID: not a UUID4')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        try:
            amenity = facade.get_amenity(amenity_id)
        except Exception as e:
            api.abort(400, str(e))
            return {'error': str(e)}, 400
        if not amenity:
            api.abort(404, error='Amenity not found')
            return {'error': 'Amenity not found'}, 404
        return amenity, 200

    @api.doc('Returns the updated amenity')
    @api.marshal_with(amenity_response_model,
                      code=_http.HTTPStatus.OK,
                      description='Amenity updated successfully')
    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Amenity not found')
    def put(self, amenity_id):
        """Update an amenity's information"""
        new_amenity_data = api.payload
        try:
            updated_amenity = facade.update_amenity(amenity_id,
                                                    new_amenity_data)
        except Exception as e:
            api.abort(400, error=str(e))
            return {'error': str(e)}, 400
        # If the amenity is not found, return an error
        # Otherwise, return the updated amenity as a dictionary
        if not updated_amenity:
            api.abort(404, error='Amenity not found')
            return {'error': 'Amenity not found'}
        return updated_amenity, 200
