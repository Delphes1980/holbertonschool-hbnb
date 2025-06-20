from app import create_app
from flask import redirect

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

##########################
########## TODO ##########
##########################
# Status code DELETE 204
# Place not found when searching all reviews for a place
# Implement PATCH if possible
# Implement Delete for all entities
# Implement add amenity
