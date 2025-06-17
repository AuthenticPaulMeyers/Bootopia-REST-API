from flask import Blueprint, request, jsonify
from ..schema.models import db, Tag, BookTag
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..constants.http_status_codes import HTTP_404_NOT_FOUND, HTTP_200_OK,HTTP_400_BAD_REQUEST, HTTP_201_CREATED

tag_bp = Blueprint('tag', __name__, static_url_path='static/', url_prefix='/api/v1.0/tags')

# get all tags
@tag_bp.route('/', methods=['POST', 'GET'])
@jwt_required()
def get_tags():

    if request.method == 'GET':
        tags = Tag.query.all()

        if not tags:
            return ({'error': 'No tags available.'}), HTTP_404_NOT_FOUND
        
        data_tag = []
        
        for tag in tags:
            data_tag.append({
                'id': tag.id,
                'name': tag.name
            })
        return ({'tags': data_tag}), HTTP_200_OK
    else:
        tag_name = request.json['name']

        if not tag_name or tag_name == '':
            return jsonify({'error': 'Required fields should not be empty.'}), HTTP_400_BAD_REQUEST
        
        tag = Tag(name=tag_name)
        db.session.add(tag)
        db.session.commit()
        return jsonify({
            'message': 'Tag added successfully.',
            'tag':{
                'name': tag_name
            }
        }), HTTP_201_CREATED
    
# delete tag
@tag_bp.route('/delete/<int:tag_id>', methods=['DELETE'])
@jwt_required()
def delete_tag(tag_id):
    tag = Tag.query.filter_by(id=tag_id).first()

    if not tag:
        return ({'error': 'Tag not found.'}), HTTP_400_BAD_REQUEST
    
    if request.method == 'DELETE':
        db.session.delete(tag)
        db.session.commit()
        return ({'message': 'Tag deleted successfully.'}), HTTP_200_OK
    return None

# attach tags to the book
@tag_bp.route('/book_tag/<int:book_id>', methods=['POST'])
@jwt_required()
def add_tag_to_book(book_id):
    # first get tag from the user and search the tag in the tags table if it exists then get the id else add it
    tag = request.json.get('tag_name')
    if not tag:
        return jsonify({'error': 'Tag name is required.'}), HTTP_400_BAD_REQUEST
    existing_tag = Tag.query.filter_by(name=tag).first()
    if existing_tag:
        tag_id = existing_tag.id
    else:
        new_tag = Tag(name=tag)
        db.session.add(new_tag)
        db.session.commit()
        tag_id = new_tag.id
    # now check if the book_tag already exists
    book_tag = BookTag.query.filter_by(book_id=book_id, tag_id=tag_id).first()
    if book_tag:
        return jsonify({'error': 'Tag already exists for this book.'}), HTTP_400_BAD_REQUEST
    new_book_tag = BookTag(book_id=book_id, tag_id=tag_id)
    db.session.add(new_book_tag)
    db.session.commit()
    return jsonify({'message': 'Tag added to book successfully.'}), HTTP_201_CREATED

# get all books with a specific tag
@tag_bp.route('/books/<int:tag_id>', methods=['GET'])
@jwt_required()
def get_books_by_tag(tag_id):
    books = BookTag.query.filter_by(tag_id=tag_id).all()
    if not books:
        return jsonify({'error': 'No books found for this tag.'}), HTTP_404_NOT_FOUND

    book_data = []
    for book in books:
        book_data.append({
            'id': book.book.id,
            'title': book.book.title,
            'author': book.book.author,
            'description': book.book.description,
            'file_url': book.book.file_url,
            'cover_image_url': book.book.cover_image_url,
        })
    return jsonify({'books': book_data}), HTTP_200_OK