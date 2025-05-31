from flask import request, redirect, url_for, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from ..schema.models import db, User

# create a blueprint for this route

users = Blueprint('users', __name__, static_url_path='static/', url_prefix='/auth')

# get a user profile route
@users.route('/<int:user_id>', methods=['POST', 'GET'])
def get_user_profile(user_id):
    return 

# update a user profile route
@users.route('/<int:user_id>', methods=['POST', 'GET'])
def update_user_profile(user_id):
    return 

# follow a user route
@users.route('/<int:user_id>/follow', methods=['POST', 'GET'])
def follow_user(user_id):
    return

# unfollow a user route
@users.route('/<int:user_id>/unfollow', methods=['POST', 'GET'])
def follow_user(user_id):
    return

# get a user profile route
@users.route('/<int:user_id>', methods=['POST', 'GET'])
def user_profile(user_id):
    return

# get user's followers route
@users.route('/<int:user_id>/followers')
def get_followers(user_id):
    return 

# get user's following route
@users.route('/<int:user_id>/following', methods=['POST', 'GET'])
def get_user_following():
    return