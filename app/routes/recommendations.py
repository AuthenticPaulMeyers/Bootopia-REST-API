from flask import request, Blueprint, jsonify
from ..constants.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST
from ..services.get_recommendations import get_mood_recommendations
from ..schema.models import db, UserRecommendation, Book
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import limiter, get_remote_address


recommender = Blueprint('recommendations', __name__, url_prefix='/api/v1.0/recommendations')

# Route to get mood-based book recommendations
@recommender.route('/mood')
@jwt_required()
@limiter.limit("10 per day", key_func=get_remote_address)
def mood_based_recommendations():
    user_id = get_jwt_identity()

    mood = request.args.get('mood')

    # Validate the mood parameter
    if not mood or not isinstance(mood, str):
        return {"error": "Mood should be a non-empty string."}, HTTP_400_BAD_REQUEST
    # Check if mood is empty
    if mood == "" or not mood:
        return {"error": "Mood should not be empty."}, HTTP_400_BAD_REQUEST
    
    mood = mood.lower().strip()

    book_recommendations = get_mood_recommendations(mood)
    if not book_recommendations:
        return {"error": "No recommendations found for the given mood."}, HTTP_400_BAD_REQUEST  
    
    book_list = book_recommendations.get('books', [])
    if not book_list:
        return {"error": "No books found in the recommendations."}, HTTP_400_BAD_REQUEST
    
    for book in book_list:
        # add the book to the database if it does not exist
        existing_book_id = Book.query.filter_by(id=book['id']).first()
        existing_book_title = Book.query.filter_by(title=book['title']).first()
        if existing_book_id or existing_book_title:
            # if the book already exists, skip adding it
            continue
        else:
            new_book = Book(
                id=book['id'],
                title=book['title'],
                author=book['author'],
                description=book['description'],
                file_url=book['file_url'],
                cover_image_url=book['cover_image_url'],
                year_published=book.get('year_published', None),
                isbn=book.get('isbn', None),
                user_id=user_id
            )
            db.session.add(new_book)
            db.session.commit()
        # Store the recommendations in the UserRecommendation table
        # Check if the recommendation already exists
        existing_recommendation = UserRecommendation.query.filter_by(
            user_id=user_id, book_id=book['id']
        ).first()
        if existing_recommendation:
            # If it exists, skip adding it
            continue
        else:
            recommendation = UserRecommendation(
                user_id=user_id,
                book_id=new_book.id
            )
            db.session.add(recommendation)
            db.session.commit()

    return jsonify({ 'data': book_recommendations }), HTTP_200_OK

# Route to get all recommendations for a user
@recommender.route('/', methods=['GET'])
@jwt_required()
def get_all_recommendations():
    user_id = get_jwt_identity()
    
    recommendations = UserRecommendation.query.filter_by(user_id=user_id).all()
    
    if not recommendations:
        return {"message": "No recommendations available."}, HTTP_400_BAD_REQUEST
    
    books = [rec.book.to_dict() for rec in recommendations]
    
    return jsonify({"recommendations": books}), HTTP_200_OK

# Route to clear all recommendations for a user
@recommender.route('/clear', methods=['DELETE'])
@jwt_required()
def clear_recommendations():
    user_id = get_jwt_identity()
    
    # Delete all recommendations for the user
    UserRecommendation.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    
    return jsonify({"message": "All recommendations cleared."}), HTTP_200_OK

# Route to delete a specific recommendation by book ID
@recommender.route('/<int:book_id>', methods=['DELETE'])
@jwt_required()
def delete_recommendation(book_id):
    user_id = get_jwt_identity()
    
    # Find the recommendation
    recommendation = UserRecommendation.query.filter_by(user_id=user_id, book_id=book_id).first()
    
    if not recommendation:
        return {"error": "Recommendation not found."}, HTTP_400_BAD_REQUEST
    
    # Delete the recommendation
    db.session.delete(recommendation)
    db.session.commit()
    
    return jsonify({"message": "Recommendation deleted successfully."}), HTTP_200_OK

# Route to get a specific recommendation by book ID
@recommender.route('/book/<int:book_id>', methods=['GET'])
@jwt_required()
def get_recommendation(book_id):
    user_id = get_jwt_identity()
    
    # Find the recommendation
    recommendation = UserRecommendation.query.filter_by(user_id=user_id, book_id=book_id).first()
    
    if not recommendation:
        return {"error": "Recommendation not found."}, HTTP_400_BAD_REQUEST
    
    book = recommendation.book.to_dict()
    
    return jsonify({"recommendation": book}), HTTP_200_OK

