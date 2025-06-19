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
                      code=_http.HTTPStatus.CREATED,
                      description='Review successfully created')
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
            return {'error': str(e)}, 400
        return review, 201

    @api.doc('Returns a list of all reviews')
    @api.marshal_list_with(review_response_model,
                      code=_http.HTTPStatus.OK,
                      description='List of reviews retrieved successfully')
    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        return facade.get_all_reviews(), 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.doc('Returns review corresponding to given ID')
    @api.marshal_with(review_response_model,
                      code=_http.HTTPStatus.OK,
                      description='Review details retrieved successfully')
    @api.response(200, 'Review details retrieved successfully')
    @api.response(400, 'Invalid ID: not a UUID4')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        try:
            review = facade.get_review(review_id)
        except Exception as e:
            api.abort(400, error=str(e))
            return {'error', str(e)}, 400
        if not review:
            api.abort(404, error='Review not found')
            return {'error': 'Review not found'}, 404
        return review, 200


    @api.doc('Returns the updated review')
    @api.marshal_with(review_response_model,
                      code=_http.HTTPStatus.OK,
                      description='Review updated successfully')
    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Review not found')
    def put(self, review_id):
        """Update a review's information"""
        review_data = api.payload
        try:
            updated_review = facade.update_review(review_id,
                                                  review_data)
        except Exception as e:
            api.abort(400, error=str(e))
            return {'error': str(e)}, 400
        if not updated_review:
            api.abort(404, error='Review not found')
            return {'error': 'Review not found'}, 404
        return updated_review, 200

    @api.doc('Deletes review')
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        try:
            facade.delete_review(review_id)
        except Exception as e:
            api.abort(404, str(e))
            return {'error': str(e)}, 404
        return f"Review {review_id} has been succesfully deleted", 200
        

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.doc('Returns the list of reviews given to the concerned '
             'place')
    @api.marshal_list_with(review_response_model,
                      code=_http.HTTPStatus.OK,
                      description='List of reviews given to the place retrieved successfully')
    @api.response(
        200, 'List of reviews for the place retrieved successfully')
    @api.response(400, 'Invalid ID')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        try:
            reviews_by_place = facade.get_reviews_by_place(place_id)
        except Exception as e:
            api.abort(400, error=str(e))
            return {'error': str(e)}, 400
        if not reviews_by_place:
            api.abort(404, error='Place not found')
            return {'error': 'Place not found'}, 404
        return reviews_by_place, 200
