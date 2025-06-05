from flask import request, Blueprint, jsonify
from ..schema.models import db, Comment
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..constants.http_status_codes import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_201_CREATED

# create a blueprint for this route
user_comments = Blueprint('comments', __name__, url_prefix='/comments')

# Comment a post
@user_comments.route('/<int:post_id>/comment', methods=['POST', 'GET'])
@jwt_required()
def comment_post(post_id):
    userId = get_jwt_identity()

    if request.method == 'POST':
        content = request.json['content']

        comment = Comment(content=content, user_id=userId, post_id=post_id)
        db.session.add(comment)
        db.session.commit()
        return jsonify({'message': 'Comment added.'}), HTTP_201_CREATED
    return jsonify({'error': 'Post not found.'}), HTTP_404_NOT_FOUND

# get comments for a specific post
@user_comments.route('/post/<int:post_id>', methods=['GET'])
@jwt_required()
def get_comment_post(post_id):

    # get comments for the post (not just by the current user)
    comments = Comment.query.filter_by(post_id=post_id).all()
    comments_count = len(comments)

    if not comments:
        return jsonify({'error': 'No available comments.'}), HTTP_404_NOT_FOUND

    comments_data = [
        {
            'id': comment.id,
            'user': getattr(comment.users, 'username', None),
            'content': comment.content,
            'date_posted': comment.posted_at
        }
        for comment in comments
    ]
    return jsonify({'comment_count': comments_count, 'comments': comments_data}), HTTP_200_OK

# delete a comment
@user_comments.route('/<int:comment_id>/delete', methods=['DELETE'])
@jwt_required()
def delete_comment(comment_id):
    userId = get_jwt_identity()
    comment = Comment.query.filter_by(id=comment_id, user_id=userId).first()

    if not comment:
        return jsonify({'error': 'Comment not found or not authorized.'}), HTTP_404_NOT_FOUND

    db.session.delete(comment)
    db.session.commit()
    return jsonify({'message': 'Comment deleted.'}), HTTP_200_OK