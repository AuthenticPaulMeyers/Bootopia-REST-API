from flask import Flask, jsonify
import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
from .schema.models import db
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from flask_migrate import Migrate
from .constants.http_status_codes import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_503_SERVICE_UNAVAILABLE, HTTP_429_TOO_MANY_REQUESTS

load_dotenv()

limiter = Limiter(
    get_remote_address,
    default_limits=["100 per day", "50 per hour"],
    storage_uri="memory://",
    strategy="moving-window",
)  

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URI'),
            JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY'),
            SQLALCHEMY_TRACK_MODIFICATIONS=False
        )
    else:
        app.config.from_mapping(test_config)
    
    # initialise the database here
    db.app=app
    db.init_app(app)
    # initialise the limiter here
    limiter.init_app(app)
    # initialise jwt here
    JWTManager(app)
    # initialise migrations
    Migrate(app, db)
    CORS(app)

    # import blueprints
    from .routes.recommendations import recommender
    from .routes.book import books
    from .auths.user_auth import auth
    from .routes.likes import user_likes
    from .routes.posts import user_posts
    from .routes.comments import user_comments
    from .routes.users import user_follow
    from .routes.summarizer import summarize
    from .routes.user_books import user_bookmarks
    from .routes.quotes import user_quotes
    from .routes.tags import tag_bp
    from .routes.notifications import notification_bp
    from .routes.feed import feed_bp

    # configure blueprints here
    app.register_blueprint(recommender)
    app.register_blueprint(books)
    app.register_blueprint(auth)
    app.register_blueprint(user_posts)
    app.register_blueprint(user_likes)
    app.register_blueprint(user_comments)
    app.register_blueprint(user_follow)
    app.register_blueprint(summarize)
    app.register_blueprint(user_bookmarks)
    app.register_blueprint(user_quotes)
    app.register_blueprint(tag_bp)
    app.register_blueprint(notification_bp)
    app.register_blueprint(feed_bp)
    
    
    # exception handling
    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_file_not_found(error):
        return jsonify({'error': f"{HTTP_404_NOT_FOUND} File not found!"}), HTTP_404_NOT_FOUND
    
    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_internalServer_error(error):
        return jsonify({'error': "Something went wrong!"}), HTTP_500_INTERNAL_SERVER_ERROR
    
    @app.errorhandler(HTTP_503_SERVICE_UNAVAILABLE)
    def handle_connection_error(error):
        return jsonify({'error': "Service is currently unavailable. Our team is working on it!"}), HTTP_503_SERVICE_UNAVAILABLE

    @app.errorhandler(HTTP_429_TOO_MANY_REQUESTS)
    def handle_too_many_requests(error):
        return jsonify({'error': "You have reached your limit for the day. Please try again after 24 hours."}), HTTP_429_TOO_MANY_REQUESTS

    return app