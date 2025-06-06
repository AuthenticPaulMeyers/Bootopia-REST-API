from flask import request, Blueprint, jsonify
from ..schema.models import db, Users, Follower
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..constants.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_204_NO_CONTENT

# Create a blueprint for this route

user_follow = Blueprint('users', __name__, url_prefix='/users')

# follow a user route
@user_follow.route('/<int:user_id>/follow', methods=['POST'])
@jwt_required()
def follow_user(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id == user_id:
        return jsonify({"error": "You cannot follow yourself."}), HTTP_400_BAD_REQUEST

    user_to_follow = Users.query.get(user_id)
    if not user_to_follow:
        return jsonify({"error": "User not found."}), HTTP_404_NOT_FOUND

    existing_follow = Follower.query.filter_by(follower_id=current_user_id, followed_id=user_id).first()
    if existing_follow:
        return jsonify({"message": "Already following this user."}), HTTP_200_OK

    new_follow = Follower(follower_id=current_user_id, followed_id=user_id)
    db.session.add(new_follow)
    db.session.commit()

    return {"message": f"You are now following {user_to_follow.username}."}, HTTP_201_CREATED

# unfollow a user route
@user_follow.route('/<int:followed_user_id>/unfollow', methods=['POST'])
def unfollow_user(followed_user_id):
    current_user_id = get_jwt_identity()
    if current_user_id == followed_user_id:
        return jsonify({"error": "You cannot unfollow yourself."}), HTTP_400_BAD_REQUEST
    
    user_to_unfollow = Users.query.get(followed_user_id)
    if not user_to_unfollow:
        return jsonify({'error': 'User not found.'}), HTTP_404_NOT_FOUND

    unfollow = Follower.query.filter_by(followed_id=followed_user_id, follower_id=current_user_id).first()
    if not unfollow:
        return jsonify({"error": "You are not following this user."}), HTTP_400_BAD_REQUEST
    
    db.session.delete(unfollow)
    db.session.commit()

    return {"message": "Successfully unfollowed."}, HTTP_201_CREATED


# get user's followers route
@user_follow.route('/<int:user_id>/followers', methods=['GET'])
def get_followers(user_id):
    user = Users.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found.'}), HTTP_404_NOT_FOUND

    followers = Follower.query.filter_by(followed_id=user_id).all()
    follower_list = [
        {
            "id": follower.follower.id,
            "username": follower.follower.username
        }
        for follower in followers if follower.follower
    ]

    return jsonify({"followers": follower_list}), HTTP_200_OK

# get user's following route
@user_follow.route('/<int:user_id>/following', methods=['GET'])
def get_user_following(user_id):
    user = Users.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found.'}), HTTP_404_NOT_FOUND

    following = Follower.query.filter_by(follower_id=user_id).all()
    following_list = [
        {
            "id": follow.followed.id,
            "username": follow.followed.username
        }
        for follow in following if follow.followed
    ]

    return jsonify({"following": following_list}), HTTP_200_OK