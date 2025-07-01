from flask_restx import Namespace, Resource, fields, _http
from app.services import facade
from app.api.v1.apiRessources import (compare_data_and_model,
                                      CustomError)
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True,
                                description='First name of the user'),
    'last_name': fields.String(required=True,
                               description='Last name of the user'),
    'email': fields.String(required=True,
                           description='Email of the user'),
    'password': fields.String(required=True,
                              description='Password of the user')
})

user_response_model = api.model('UserResponse', {
    'id': fields.String(required=True,
                        description='ID of the user'),
    'first_name': fields.String(required=True,
                                description='First name of the user'),
    'last_name': fields.String(required=True,
                               description='Last name of the user'),
    'email': fields.String(required=True,
                           description='Email of the user')
})

error_model = api.model('Error', {
    'error': fields.String(description='Error message')
})

@api.route('/')
class UserList(Resource):
    @api.doc('Returns the created user')
    @api.marshal_with(user_response_model,
                      code=_http.HTTPStatus.CREATED,
                      description='User successfully created')
    @api.expect(user_model, validate=False)
    @api.response(201, 'User successfully created',
                  user_response_model)
    @api.response(400, 'Email already registered / Invalid input data',
                  error_model)
    def post(self):
        """Register a new user"""
        user_data = api.payload
        try:
            compare_data_and_model(user_data, user_model)
            new_user = facade.create_user(user_data)
        except Exception as e:
            api.abort(400, error=str(e))
            return {'error': str(e)}, 400
        return new_user, 201
    
    @api.doc('Returns list of registered users')
    @api.marshal_list_with(user_response_model,
                      code=_http.HTTPStatus.OK,
                      description='List of users retrieved '
                                  'successfully')
    @api.response(200, 'List of users retrieved successfully',
                  user_response_model)
    def get(self):
        """Get a list of registered users"""
        return facade.get_all_users(), 200

@api.route('/<user_id>')
class UserResource(Resource):
    @api.doc('Returns user corresponding to given ID')
    @api.marshal_with(user_response_model,
                      code=_http.HTTPStatus.OK,
                      description='User details retrieved successfully')
    @api.response(200, 'User details retrieved successfully',
                  user_response_model)
    @api.response(400, 'Invalid ID: not a UUID4 / Invalid input data',
                  error_model)
    @api.response(404, 'User not found', error_model)
    def get(self, user_id):
        """Get user details by ID"""
        try:
            user = facade.get_user(user_id)
        except Exception as e:
            api.abort(400, error=str(e))
            return {'error', str(e)}, 400
        if not user:
            api.abort(404, error='User not found')
            return {'error': 'User not found'}, 404
        return user, 200

    @api.doc('Returns the updated user', security='Bearer')
    @api.marshal_with(user_response_model,
                      code=_http.HTTPStatus.OK,
                      description='User updated successfully')
    @api.expect(user_model, validate=False)
    @api.response(200, 'User successfully updated',
                  user_response_model)
    @api.response(400, 'Invalid input data', error_model)
    @api.response(403, 'Unauthorized action', error_model)
    @api.response(401, 'Missing authorization header', error_model)
    @api.response(404, 'User not found', error_model)
    @jwt_required() # ensure the user is authenticated
    def put(self, user_id):
        """Update the user data of a registered user by ID"""
        user_data = api.payload
        try:
            compare_data_and_model(user_data, user_model)
            current_user = get_jwt_identity()
            if current_user != user_id: # check the user_id in the URL 
                                    # matches the authenticated user
                raise CustomError('Unauthorized action', 403)
            user = facade.get_user(user_id)
            if (user.email != user_data.get("email") or
                not user.verify_password(user_data.get("password"))):
                raise CustomError('You cannot modify email or password action', 400)
            updated_user = facade.update_user(user_id, user_data)
        except CustomError as e:
            api.abort(e.status_code, error=str(e))
            return {'error': str(e)}, e.status_code
        except Exception as e:
            api.abort(400, error=str(e))
            return {'error': str(e)}, 400
        if not updated_user:
            api.abort(404, error='User not found')
            return {'error': 'User not found'}, 404
        return updated_user, 200
