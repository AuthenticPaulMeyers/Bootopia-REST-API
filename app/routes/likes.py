from flask import request, Blueprint, jsonify
from ..schema.models import db, Likes, Users, Notification, Post
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..constants.http_status_codes import HTTP_200_OK, HTTP_404_NOT_FOUND

# create a blueprint for this route
user_likes = Blueprint('likes', __name__, url_prefix='/api/v1.0/likes')

# Like and unlike a post
@user_likes.route('/<int:post_id>/like', methods=['POST', 'GET'])
@jwt_required()
def like_post(post_id):
    userId = get_jwt_identity()
    current_user = Users.query.get(userId)
    # get post with that id
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found.'}), HTTP_404_NOT_FOUND
    
    # Allow users to like a post
    existing_like = Likes.query.filter_by(user_id=userId, post_id=post_id).first()
    if existing_like:
         # allow users to unlike a post if the post alreaady exists
        db.session.delete(existing_like)
        db.session.commit()
        return jsonify({'message': 'Post unliked successfully.'}), HTTP_200_OK
    
    if request.method == 'POST':
        like = Likes(user_id=userId, post_id=post_id)
        db.session.add(like)
        db.session.commit()

        message = f"{current_user.username} liked your post."
        notification = Notification(user_id=post.users.id, message=message)
        db.session.add(notification)
        db.session.commit()
        return jsonify({'message': 'Liked a post.'}), HTTP_200_OK
    return jsonify({'error': 'Post not found.'}), HTTP_404_NOT_FOUND
