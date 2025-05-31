from flask import request, redirect, url_for, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from ..schema.models import db, User

# create a blueprint for this route

auth = Blueprint('auth', __name__, static_url_path='static/', url_prefix='/auth')

# register route
@auth.route('/register', methods=['POST', 'GET'])
def register_user():
    return 

# login route
@auth.route('/login', methods=['POST', 'GET'])
def login_user():
    return

# get current user profile route
@auth.route('/me', methods=['POST', 'GET'])
def current_user_profile():
    return

# logout user route
@auth.route('/logout', methods=['POST', 'GET'])
def logout_user():
    return