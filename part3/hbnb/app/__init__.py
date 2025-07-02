from flask import Flask
from flask_restx import Api

# from app.api.v1.amenities import api as amenities_ns
# from app.api.v1.places import api as places_ns
# from app.api.v1.users import api as users_ns
# from app.api.v1.reviews import api as reviews_ns
# from app.api.v1.auth import api as auth_ns

from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

bcrypt = Bcrypt()
jwt = JWTManager()

authorizations = {
    'Bearer': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': (
            'JWT Authorization header using the Bearer scheme.\n'
            'Enter your JWT token as: Bearer &lt;your_token&gt;\n\n'
            'Example: <code>Bearer eyJhbGciOiJIUzI1NiIsInR5...</code>')
    }
}

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)
    # app.config['ERROR_INCLUDE_MESSAGE'] = False
    bcrypt.init_app(app)
    jwt.init_app(app)

    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.users import api as users_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.auth import api as auth_ns

    api = Api(app, version='1.0', title='HBnB API',
              description='HBnB Application API', doc='/api/v1/',
              authorizations=authorizations)
    
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')

    return app
