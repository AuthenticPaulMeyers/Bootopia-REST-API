from flask import Flask
import os
from .schema.models import db
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from .routes.recommendations import recommender
from .routes.book import books
from .auths.user_auth import auth
from .routes.likes import likes
from .routes.posts import posts

load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL'),
            JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY'),
            SQLALCHEMY_TRACK_MODIFICATIONS=False
           
        )
    else:
        app.config.from_mapping(test_config)
    
    # initialise the database here
    db.app=app
    db.init_app(app)
    
    # initialise jwt here
    JWTManager(app)

    # configure blueprints here
    app.register_blueprint(recommender)
    app.register_blueprint(books)
    app.register_blueprint(auth)
    app.register_blueprint(posts)
    app.register_blueprint(likes)
    

    # exception handling
    # @app.errorhandler(HTTP_404_NOT_FOUND)
    # def handle_file_not_found(error):
    #     return jsonify({'error': f"{HTTP_404_NOT_FOUND} File not found!"}), HTTP_404_NOT_FOUND
    
    # @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    # def handle_internalServer_error(error):
    #     return jsonify({'error': "Something went wrong!"}), HTTP_500_INTERNAL_SERVER_ERROR
    
    # @app.errorhandler(HTTP_503_SERVICE_UNAVAILABLE)
    # def handle_connection_error(error):
    #     return jsonify({'error': "Service is currently unavailable. Our team is working on it!"}), HTTP_503_SERVICE_UNAVAILABLE

    return app