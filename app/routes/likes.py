from flask import request, Blueprint, jsonify
from ..schema.models import db, Like, Post
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..constants.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_204_NO_CONTENT

# create a blueprint for this route
likes = Blueprint('likes', __name__, static_url_path='static/', url_prefix='/likes')


# Like a post
@likes.route('/<int:post_id>', methods=['POST', 'GET'])
@jwt_required()
def get_post(post_id):
    return 

# Unlike a post
@likes.route('/<int:post_id>', methods=['POST', 'GET'])
@jwt_required()
def get_post(post_id):
    return 