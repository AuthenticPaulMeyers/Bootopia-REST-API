from flask import request, redirect, url_for, Blueprint
from ..schema.models import db, Post

# create a blueprint for this route

posts = Blueprint('posts', __name__, static_url_path='static/', url_prefix='/posts')

# create recent posts
@posts.route('/', methods=['POST', 'GET'])
def posts():
    return 

# create recent posts
@posts.route('/create_post', methods=['POST', 'GET'])
def create_post():
    return 

# get a specific post
@posts.route('/<int:post_id>', methods=['POST', 'GET'])
def get_post(post_id):
    return

# update a specific post
@posts.route('/<int:post_id>', methods=['POST', 'GET'])
def update_post(post_id):
    return

# delete a specific post
@posts.route('/<int:post_id>', methods=['POST', 'GET'])
def delete_post(post_id):
    return

