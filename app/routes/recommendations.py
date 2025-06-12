from flask import request, Blueprint
from ..constants.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST
from ..services.get_recommendations import get_mood_recommendations
from ..schema.models import db
from flask_jwt_extended import jwt_required, get_jwt_identity

recommender = Blueprint('recommendations', __name__, url_prefix='/api/v1.0/recommendations')

@recommender.route('/mood')
@jwt_required()
def mood_based_recommendations():
    mood = request.args.get('mood')

    if mood == "":
        return {"error": "Mood should not be empty."}, HTTP_400_BAD_REQUEST

    book_recommendations = get_mood_recommendations(mood)
    # write some code to save the recommendations in the database table
    # 
    # 

    return {
        'recommendations': book_recommendations
    }, HTTP_200_OK

@recommender.route('/')
@jwt_required()
def user_based_recommendations():
    return True