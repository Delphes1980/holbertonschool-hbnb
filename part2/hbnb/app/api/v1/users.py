from flask_restx import Namespace, Resource, fields, _http
from app.services import facade
from app.api.v1.apiRessources import compare_data_and_model

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True,
                                description='First name of the user'),
    'last_name': fields.String(required=True,
                               description='Last name of the user'),
    'email': fields.String(required=True,
                           description='Email of the user')
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

@api.route('/')
class UserList(Resource):
    @api.doc('Returns the created user')
    @api.marshal_with(user_response_model,
                      code=_http.HTTPStatus.CREATED,
                      description='User successfully created')
    @api.expect(user_model, validate=False)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered / Invalid input data')
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
    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Get a list of registered users"""
        return facade.get_all_users(), 200

@api.route('/<user_id>')
class UserResource(Resource):
    @api.doc('Returns user corresponding to given ID')
    @api.marshal_with(user_response_model,
                      code=_http.HTTPStatus.OK,
                      description='User details retrieved successfully')
    @api.response(200, 'User details retrieved successfully')
    @api.response(400, 'Invalid ID: not a UUID4')
    @api.response(404, 'User not found')
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

    @api.doc('Returns the updated user')
    @api.marshal_with(user_response_model,
                      code=_http.HTTPStatus.OK,
                      description='User updated successfully')
    @api.expect(user_model, validate=False)
    @api.response(200, 'User successfully updated')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update the user data of a registered user by ID"""
        user_data = api.payload
        try:
            compare_data_and_model(user_data, user_model)
            updated_user = facade.update_user(user_id, user_data)
        except Exception as e:
            api.abort(400, error=str(e))
            return {'error': str(e)}, 400
        if not updated_user:
            api.abort(404, error='User not found')
            return {'error': 'User not found'}, 404
        return updated_user, 200
