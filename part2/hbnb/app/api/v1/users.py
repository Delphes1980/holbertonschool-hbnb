from flask_restx import Namespace, Resource, fields
from app.services import facade
from uuid import UUID

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


@api.route('/')
class UserList(Resource):
    # Endpoint for creating a new user
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered / Invalid input data')
    def post(self):
        """Register a new user
        Possible 400 errors:
        - Email already registered
        - Invalid input data
        """
        user_data = api.payload

        # Simulate email uniqueness check (to be replaced by real validation
        # with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        try:
            # Call facade to create user
            new_user = facade.create_user(user_data)
        except Exception as e:
            return {'error': str(e)}, 400

        # Return the newly created user's details
        return {'id': new_user.id, 'first_name': new_user.first_name,
                'last_name': new_user.last_name, 'email': new_user.email}, 201

    # Endpoint for retrieving all registered users
    @api.doc('Returns list of registered users')
    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Get a list of registered users"""
        # Retrieve all users from the repository
        # Convert each user object to a dictionary for the response
        user_list = facade.user_repo.get_all()
        return [{'id': user.id, 'first_name': user.first_name, 'last_name':
                user.last_name, 'email': user.email} for user in
                user_list], 200


@api.route('/<user_id>')
class UserResource(Resource):
    # Endpoint for retrieving a single user by ID
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    @api.response(400, "Invalid UUID: User ID must be a UUID")
    def get(self, user_id):
        """Get user details by ID"""
        try:
            # Validate is user_id is a valid UUID
            UUID(user_id)
        except ValueError:
            return {'error': 'Invalid UUID'}, 400

        # Retrieve user from facade
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        # Return the user's details
        return {'id': user.id, 'first_name': user.first_name, 'last_name':
                user.last_name, 'email': user.email}, 200

    # Endpoint for updating an existing user by ID
    @api.expect(user_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User_id does not correspond to any registered'
                  ' user')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """Update the user data of a registered user by ID"""
        try:
            # Validate is user_id is a valid UUID
            UUID(user_id)
        except ValueError:
            return {'error': 'Invalid UUID'}, 400

        user_by_id = facade.get_user(user_id)  # Get user by ID
        if not user_by_id:
            return {'error': 'User does not exist'}, 404

        # Get updated user data from request body
        user_data = api.payload
        # Check for existing email
        user_by_email = facade.get_user_by_email(user_data["email"])

        # Prevent updating to an email already registered by another user
        if (user_by_email and
                user_by_email.id != user_by_id.id):
            return {'error': 'email already registered with another '
                    'account'}, 400
        try:
            # Update user via facade/repository
            facade.user_repo.update(user_id, user_data)
        except Exception as e:
            return {'error': str(e)}, 400
        return {'id': user_by_id.id,
                'first_name': user_by_id.first_name,
                'last_name': user_by_id.last_name,
                'email': user_by_id.email}, 200
