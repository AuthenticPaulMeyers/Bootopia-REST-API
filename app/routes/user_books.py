from flask import request, Blueprint, jsonify
from ..schema.models import db, UserBook
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..constants.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_204_NO_CONTENT


# create a blueprint for this route
user_bookmarks = Blueprint('bookmark', __name__, static_url_path='static/', url_prefix='/api/v1.0/bookmarks')

# get all bookmarks
@user_bookmarks.route('/')
@jwt_required()
def get_all_bookmarks():
    user_id = get_jwt_identity()

    # get all bookmarks
    all_bookmarks = UserBook.query.filter_by(user_id=user_id).all()

    if not all_bookmarks:
        return jsonify({'message': 'No bookmarks currently available.'}), HTTP_200_OK
    
    bookmark_data = []

    for bookmark in all_bookmarks:
        bookmark_data.append({
            'id': bookmark.id,
            'book_title': bookmark.book.title,
            'book_author': bookmark.book.author,
            'book_description': bookmark.book.description,
            'book_file_url': bookmark.book.file_url,
            'book_cover_image_url': bookmark.book.cover_image_url,
        })
    return ({'bookmarks': bookmark_data}), HTTP_200_OK

# add to bookmarks
@user_bookmarks.route('/add/<int:book_id>/', methods=['POST'])
@jwt_required()
def add_bookmarks(book_id):
    user_id = get_jwt_identity()

    if request.method == 'POST':
        bookmark = UserBook(user_id=user_id, book_id=book_id)
        db.session.add(bookmark)
        db.session.commit()
        return jsonify({'message': 'Successfully added to bookmarks.'}), HTTP_201_CREATED
    else:
        return None

# Remove from bookmark
@user_bookmarks.route('/<int:bookmark_id>/remove', methods=['DELETE'])
@jwt_required()
def delete_bookmarks(bookmark_id):
    user_id = get_jwt_identity()
    bookmark = UserBook.query.filter_by(user_id=user_id, id=bookmark_id).first()

    if not bookmark:
        return jsonify({'error': 'Bookmark not found.'}), HTTP_404_NOT_FOUND
    
    if request.method == 'DELETE':

        db.session.delete(bookmark)
        db.session.commit()
        return jsonify({'message': 'Successfully removed from bookmarks.'}), HTTP_200_OK
    else:
        return None
    
# Clear all bookmarks
@user_bookmarks.route('/clear', methods=['DELETE'])
@jwt_required()
def clear_bookmarks():
    user_id = get_jwt_identity()
    
    if request.method == 'DELETE':
        bookmarks = UserBook.query.filter_by(user_id=user_id).all()

        if not bookmarks:
            return jsonify({'message': 'No bookmarks available.'}), HTTP_200_OK
        
        for bookmark in bookmarks:
            db.session.delete(bookmark)
        
        db.session.commit()
        return jsonify({'message': 'Bookmarks cleared successfully.'}), HTTP_204_NO_CONTENT

