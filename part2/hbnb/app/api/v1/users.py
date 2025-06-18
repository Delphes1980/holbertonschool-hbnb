from flask_restx import Namespace, Resource, fields, _http
from app.services import facade
from uuid import UUID

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('UserData', {
    'first_name': fields.String(required=True,
                                description='First name of the user'),
    'last_name': fields.String(required=True,
                               description='Last name of the user'),
    'email': fields.String(required=True,
                           description='Email of the user')
})

user_response_model = api.inherit('UserResponse', user_model, {
    'id': fields.String(required=True,
                        description='User uuid4')
})

def is_valid_uuid4(uuid_str):
    """Determines if given str is a uuid4"""
    try:
        val = UUID(uuid_str, version=4)
        return val.version == 4
    except ValueError:
        return False

@api.route('/')
class UserList(Resource):
    @api.doc(description="Returns the new user")
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered / Invalid input data')
    # @api.marshal_with(user_response_model,
    #                   code=_http.HTTPStatus.CREATED)
    def post(self):
        """Register a new user"""
        user_data = api.payload
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400
        try:
            new_user = facade.create_user(user_data)
        except Exception as e:
            return {'error': str(e)}, 400
        return {'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email}, 201
    
    @api.doc(description="Returns a list of all users in the system")
    @api.response(200, 'User list successfully retrieved')
    # @api.marshal_list_with(user_response_model)
    def get(self):
        """Get a list of registered users"""
        user_list = facade.get_all_users()
        return [{'id': user.id,
                 'first_name': user.first_name,
                 'last_name': user.last_name,
                 'email': user.email}
                 for user in user_list], 200

@api.route('/<user_id>')
class UserResource(Resource):
    @api.doc(description="Returns the user corresponding to that ID")
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    @api.response(400, "Invalid UUID: User ID must be a UUID")
    # @api.marshal_with(user_response_model)
    def get(self, user_id):
        """Get user details given its ID"""
        if not is_valid_uuid4(user_id):
            return {'error': 'Invalid UUID'}, 400
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email}, 200

    @api.doc(description="Returns the updated user")
    @api.expect(user_model, validate=True)
    @api.response(204, 'User data properly updated to new data')
    @api.response(404, 'User_id does not correspond to any registered'
                  ' user')
    @api.response(400, 'Invalid input data')
    @api.response(500, 'Failure to retrieve user after update')
    # @api.marshal_with(user_response_model)
    def put(self, user_id):
        """Update the user data of a registered user given its ID"""
        if not is_valid_uuid4(user_id):
            return {'error': 'Invalid UUID'}, 400
        user_by_id = facade.get_user(user_id)
        if not user_by_id:
            return {'error': 'User not found'}, 404
        user_data = api.payload
        user_by_email = facade.get_user_by_email(user_data["email"])
        if (user_by_email and
                user_by_email.id != user_by_id.id):
            return {'error': 'email already registered with another '
                    'account'}, 400
        try:
            updated_user = facade.update_user(user_id, user_data)
        except Exception as e:
            return {'error': str(e)}, 400
        if not updated_user:
            return {'error': 'user update failed'}, 500
        return {'id': updated_user.id, 
                'first_name': user_by_id.first_name,
                'last_name': user_by_id.last_name,
                'email': user_by_id.email}, 204
