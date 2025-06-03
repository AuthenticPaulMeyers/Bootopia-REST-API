from flask import request, Blueprint
from ..schema.models import db, Post
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..constants.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_201_CREATED
from ..utils.file_upload import upload_file
from ..utils.image_upload import upload_image

# create a blueprint for this route
posts = Blueprint('posts', __name__, static_url_path='static/', url_prefix='/posts')

# get all posts
@posts.route('/')
@jwt_required()
def posts():

    posts = Post.query.all()
    return 

# create a posts
@posts.route('/create_post', methods=['POST', 'GET'])
@jwt_required()
def create_post():
    userId = get_jwt_identity()

    return 

# get a specific post
@posts.route('/<int:post_id>', methods=['POST', 'GET'])
@jwt_required()
def get_post(post_id):
    return

# update a specific post
@posts.route('/edit/<int:post_id>', methods=['PUT', 'GET'])
@jwt_required()
def update_post(post_id):
    return

# delete a specific post
@posts.route('/delete/<int:post_id>', methods=['DELETE', 'GET'])
@jwt_required()
def delete_post(post_id):
    return

