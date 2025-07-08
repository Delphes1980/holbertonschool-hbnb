from flask_restx import Namespace, Resource, fields, _http
from app.services import facade
from app.api.v1.apiRessources import (compare_data_and_model,
                                      CustomError)
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt


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

error_model = api.model('Error', {
    'error': fields.String(description='Error message')
})

# Define the response model for returning amenity data
# amenity_response_model = api.inherit('AmenityResponse', amenity_model, {
#     'id': fields.String(
#         required=True,
#         description='Unique identifier for the amenity'),
# 'created_at': fields.DateTime(dt_format='iso8601', description=
# 'Timestamp of creation (ISO 8601)'),
# 'updated_at': fields.DateTime(dt_format='iso8601', description=
# 'Timestamp of the last update (ISO 8601)')
# })


class AdminAmenityCreate(Resource):
    # Endpoint for creating a new amenity
    @api.doc('Returns the created amenity', security='Bearer')
    @api.marshal_with(amenity_response_model,
                      code=_http.HTTPStatus.CREATED,
                      description='Amenity successfully created')
    @api.expect(amenity_model, validate=False)
    @api.response(201, 'Amenity successfully created',
                  amenity_response_model)
    @api.response(400, 'Name already assigned / Invalid input data', error_model)
    @jwt_required()
    def post(self):
        """Register a new amenity"""
        is_admin = get_jwt().get('is_admin', False)
        amenity_data = api.payload
        try:
            # if is_admin is None:
            #     raise CustomError('is_admin claim was not found in the jwt', 401)
            if not is_admin:
                raise CustomError('Unauthorized action: admin privileges required', 403)
            compare_data_and_model(amenity_data, amenity_model)
            new_amenity = facade.create_amenity(amenity_data)
        except CustomError as e:
            api.abort(e.status_code, error=str(e))
            return {'error': str(e)}, e.status_code
        except Exception as e:
            api.abort(400, error=str(e))
            return {'error': str(e)}, 400
        return new_amenity, 201

@api.route('/')
class AmenityList(AdminAmenityCreate):
    # Endpoint for retrieving all amenities
    @api.doc('Returns a list of all registered amenities')
    @api.marshal_list_with(
        amenity_response_model,
        code=_http.HTTPStatus.OK,
        description='List of amenities retrieved successfully')
    @api.response(200, 'List of amenities retrieved successfully', amenity_response_model)
    def get(self):
        """Retrieve a list of all amenities"""
        return facade.get_all_amenities(), 200
        # amenities = facade.get_all_amenities()
        # return [amenity.to_dict() for amenity in amenities], 200


class AdminAmenityModify(Resource):
    # Endpoint for updating an existing amenity by ID
    @api.doc('Returns the updated amenity', security='Bearer')
    @api.marshal_with(amenity_response_model,
                      code=_http.HTTPStatus.OK,
                      description='Amenity updated successfully')
    @api.expect(amenity_model, validate=False)
    @api.response(200, 'Amenity updated successfully', amenity_response_model)
    @api.response(400, 'Invalid input data', error_model)
    @api.response(403, 'Unauthorized action', error_model)
    @api.response(404, 'Amenity not found', error_model)
    @jwt_required()
    def put(self, amenity_id):
        """Update an amenity's information"""
        is_admin = get_jwt().get('is_admin')
        amenity_data = api.payload
        try:
            if is_admin is None:
                raise CustomError('is_admin claim was not found in the jwt', 401)
            elif not is_admin:
                raise CustomError('Admin privileges required', 403)
            compare_data_and_model(amenity_data, amenity_model)
            updated_amenity = facade.update_amenity(amenity_id,
                                                    amenity_data)
        except CustomError as e:
            api.abort(e.status_code, error=str(e))
            return {'error': str(e)}, e.status_code
        except Exception as e:
            api.abort(400, error=str(e))
            return {'error': str(e)}, 400
        # If the amenity is not found, return an error
        # Otherwise, return the updated amenity as a dictionary
        if updated_amenity is None:
            api.abort(404, error='Amenity not found')
            return {'error': 'Amenity not found'}, 404
        return updated_amenity, 200


@api.route('/<amenity_id>')
class AmenityResource(AdminAmenityModify):
    # ENdpoint for retrieving a single amenity by ID
    @api.doc('Returns amenity corresponding to given ID')
    @api.marshal_with(
        amenity_response_model,
        code=_http.HTTPStatus.OK,
        description='Amenity details retrieved successfully')
    @api.response(200, 'Amenity details retrieved successfully', amenity_response_model)
    @api.response(400, 'Invalid ID: not a UUID4 / Invalid input data', error_model)
    @api.response(403, 'Unauthorized action', error_model)
    @api.response(404, 'Amenity not found', error_model)
    def get(self, amenity_id):
        """Get amenity details by ID"""
        try:
            amenity = facade.get_amenity(amenity_id)
        except Exception as e:
            api.abort(400, error=str(e))
            return {'error': str(e)}, 400
        if amenity is None:
            api.abort(404, error='Amenity not found')
            return {'error': 'Amenity not found'}, 404
        return amenity, 200
