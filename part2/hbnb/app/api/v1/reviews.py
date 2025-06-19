from flask_restx import Namespace, Resource, fields, _http
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

review_response_model = api.model('ReviewResponse', {
    'id': fields.String(required=True, description='ID of the review'),
    'user_id': fields.String(
        attribute=lambda review: f"{review.user.id}",
        required=True, description='ID of the user'),
    'place_id': fields.String(
        attribute=lambda review: f"{review.place.id}",
        required=True, description='ID of the place'),
    'text': fields.String(required=True,
                          description='Text of the review'),
    'rating': fields.Integer(required=True,
                             description='Rating of the place (1-5)')
})

@api.route('/')
class ReviewList(Resource):
    @api.doc('Returns the created review')
    @api.marshal_with(review_response_model,
                      code=_http.HTTPStatus.CREATED)
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        review_data = api.payload
        try:
            review = facade.create_review(review_data)
        except Exception as e:
            api.abort(400, error=str(e))
            return {'error', str(e)}, 400
        return review, 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        # Placeholder for logic to return a list of all reviews
        pass

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        # Placeholder for the logic to retrieve a review by ID
        pass

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        # Placeholder for the logic to update a review by ID
        pass

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        # Placeholder for the logic to delete a review
        pass

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        # Placeholder for logic to return a list of reviews for a place
        pass