from flask import Blueprint, request, jsonify
from ..schema.models import db, Book, Post, Likes, PostMood, BookMood, UserMood, Comment, Follower, UserRecommendation
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..constants.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_201_CREATED
from sqlalchemy import func, or_

feed_bp = Blueprint('feeds', __name__, static_url_path="/static", url_prefix="/api/v1.0/feeds")

"""
    Get feeds based on user recommendations
    Return a mixed feed:
      1. Posts from people user follows
      2. Posts tagged with user's active moods
      3. Posts about books the recommendation engine cached
    Ordered by: freshness + light popularity boost
"""

@feed_bp.route("/", methods=["GET"])
@jwt_required()
def get_feeds():
    user_id = get_jwt_identity()

    # 1. Define the popularity calculation as a SQL expression
    popularity = (
        func.coalesce(func.count(Likes.id), 0) * 0.5 +
        func.coalesce(func.count(Comment.id), 0) * 0.3
    ).label("pop_score")

    # 2. Get the current user's following list
    followed = db.session.query(Follower.following_id).filter(Follower.follower_id == user_id).subquery()

    # 3. get the current users active moods
    active_moods = db.session.query(UserMood.mood_id).filter(UserMood.user_id == user_id).subquery()

    # 4. Get stored book recommendations
    rec_books = db.session.query(UserRecommendation.book_id).filter(UserRecommendation.user_id == user_id).subquery()

    feed_query = (
        db.session.query(Post)
          .outerjoin(Likes, Likes.post_id == Post.id)
          .outerjoin(Comment, Comment.post_id == Post.id)
          .outerjoin(PostMood, PostMood.post_id == Post.id)
          .filter(
              or_(
                  Post.user_id.in_(followed),
                  PostMood.mood_id.in_(active_moods),
                  Post.book_id.in_(rec_books)
              )
          )
          .group_by(Post.id)
          .order_by(Post.posted_at.desc(), popularity.desc())
    )

    feed_results = feed_query.all()

    # Process results: extract Post objects and convert to dictionary
    posts = []
    for post_obj in feed_results:
        # Pass current_user_id to to_dict if needed for personalization
        post_dict = post_obj.to_dict(user_id=user_id)
        posts.append(post_dict)

    if not posts or posts == "" or posts == []:
        return jsonify({"message": "No posts currently available."}), HTTP_200_OK
    return jsonify(posts), HTTP_200_OK