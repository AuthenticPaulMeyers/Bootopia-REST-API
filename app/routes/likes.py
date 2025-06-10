from flask import request, Blueprint, jsonify
from ..schema.models import db, Like
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..constants.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

# create a blueprint for this route
user_likes = Blueprint('likes', __name__, url_prefix='/likes')

# Like a post
@user_likes.route('/<int:post_id>/like', methods=['POST', 'GET'])
@jwt_required()
def like_post(post_id):
    userId = get_jwt_identity()

    # Allow users to like a post
    existing_like = Like.query.filter_by(user_id=userId, post_id=post_id).first()
    if existing_like:
        return jsonify({'error': 'Post already liked.'}), HTTP_400_BAD_REQUEST

    if request.method == 'POST':
        like = Like(user_id=userId, post_id=post_id)
        db.session.add(like)
        db.session.commit()
        
        return jsonify({'message': 'Liked a post.'}), HTTP_200_OK
    return jsonify({'error': 'Post not found.'}), HTTP_404_NOT_FOUND

# Unlike a post
@user_likes.route('/<int:post_id>/unlike', methods=['POST', 'GET'])
@jwt_required()
def unlike_post(post_id):
    userId = get_jwt_identity()

    # allow users to unlike a post
    if request.method == 'POST':
        like = Like.query.filter_by(user_id=userId, post_id=post_id).first()
        if like:
            db.session.delete(like)
            db.session.commit()
            return jsonify({'message': 'Post unliked successfully.'}), HTTP_200_OK
        return jsonify({'error': 'Like not found.'}), HTTP_404_NOT_FOUND
    return jsonify({'error': 'Post not found.'}), HTTP_404_NOT_FOUND