from flask import request, Blueprint
from ..constants.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST
from ..services.get_recommendations import get_mood_recommendations

recommender = Blueprint('recommendations', __name__, url_prefix='/recommendations')

@recommender.route('/mood')
def mood_based_recommendations():
    mood = request.args.get('mood')

    if mood == "":
        return {"error": "Mood should not be empty."}, HTTP_400_BAD_REQUEST

    book_recommendations = get_mood_recommendations(mood)

    return {
        'recommendations': book_recommendations
    }, HTTP_200_OK

@recommender.route('/')
def user_based_recommendations():
    user_id = request.args.get('user_id')

    if user_id == "":
        return {"error": "User not found."}, HTTP_400_BAD_REQUEST