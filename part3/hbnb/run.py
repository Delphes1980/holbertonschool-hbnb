from app import create_app
from flask import redirect

app = create_app(config_class="config.DevelopmentConfig")

if __name__ == '__main__':
    app.run()

##########################
########## TODO ##########
##########################
# Status code DELETE 204
# Place not found when searching all reviews for a place
# Implement PATCH if possible
# Implement Delete for all entities
# Implement add amenity
# Place does not expect keyword amenities
# fields=0 are taken as non given (latitude/longitude/price...)
# Check that email and name (unique keys) are case-independent and that
#   name is independent of number of spaces between words
# Error due to conflict (e.g., Amenity name already exists) is code 409
# Add a message to all server responses: "{{msg: User created
# successfully}, {id: "00diunfw", name: "john", ...}} instead of just
# the object or the error message.
# Avoid amenities with same name with just different capitalization
# Avoid adding the same amenitiy multiple times to a Place
