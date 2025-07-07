from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()

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
    db.init_app(app)

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

    with app.app_context():
        db.create_all()
        from app.models.user import User
        # Only add admin and regular a user if no users exist:
        if User.query.count() == 0:
            admin_email = app.config.get('ADMIN_EMAIL', None)
            admin_password = app.config.get('ADMIN_PASSWORD', None)
            if admin_email is not None and admin_password is not None:
                admin_user = User(
                    first_name='Admin',
                    last_name='User',
                    email=admin_email,
                    password=admin_password,
                    is_admin=True
                )
                db.session.add(admin_user)
                db.session.commit()
            regular_user_email = app.config.get('REGULAR_USER_EMAIL', None)
            regular_user_password = app.config.get('REGULAR_USER_PASSWORD', None)
            if regular_user_email is not None and regular_user_password is not None:
                regular_user = User(
                    first_name='Regular',
                    last_name='User',
                    email=regular_user_email,
                    password=regular_user_password,
                    is_admin=False
                )
                db.session.add(regular_user)
                db.session.commit()
            from .models.amenity import Amenity
            if Amenity.query.filter_by(name="WiFi").first() is None:
                basic_amenity = Amenity(name="WiFi")
                db.session.add(basic_amenity)
                db.session.commit()

    return app
