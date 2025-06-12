from flask import request, Blueprint, jsonify
from ..schema.models import db, Quote, Book
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..constants.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_204_NO_CONTENT

# create a blueprint for this route
user_quotes = Blueprint('quotes', __name__, static_url_path='static/', url_prefix='/quotes')

# get all user quotes
@user_quotes.route('/')
@jwt_required()
def get_user_quotes():

    user_id = get_jwt_identity()
    quotes = Quote.query.filter_by(user_id=user_id).all()

    if not quotes:
        return jsonify({'message': 'No quotes currently available!'}), HTTP_204_NO_CONTENT

    quotes_data = []
    for quote in quotes:
        quotes_data.append({
            'id': quote.id,
            'book_title': quote.book.title,
            'content': quote.content,
            'date_created': quote.posted_at,            
        })

    return jsonify({'quotes': quotes_data}), HTTP_200_OK

# get all posts for a specific book
@user_quotes.route('/book/<int:book_id>')
@jwt_required()
def get_book_quotes(book_id):

    user_id = get_jwt_identity()
    quotes = Quote.query.filter_by(user_id=user_id, book_id=book_id).all()

    if not quotes:
        return jsonify({'message': 'No quotes currently available!'}), HTTP_204_NO_CONTENT

    quotes_data = []
    for quote in quotes:
        quotes_data.append({
            'id': quote.id,
            'book_title': quote.book.title,
            'content': quote.content,
            'date_created': quote.created_at,            
        })

    return jsonify({'book_quotes': quotes_data}), HTTP_200_OK

# create a quote
@user_quotes.route('/book/<int:book_id>/new', methods=['POST', 'GET'])
@jwt_required()
def create_new_book_quote(book_id):
    user_id = get_jwt_identity()

    if request.method == 'POST':
        content = request.json['content']

        if not content or content == '':
            return jsonify({'error': 'Missing required fields.'}), HTTP_400_BAD_REQUEST
        
        # check the book if it exists
        book = Book.query.filter_by(id=book_id).first()
        if not book:
            return jsonify({'error': 'Book not found.'}), HTTP_404_NOT_FOUND
        
        quote = Quote(user_id=user_id, book_id=book_id, content=content)
        db.session.add(quote)
        db.session.commit()

        return jsonify({
            'message': 'Quote added successfully!',
            'quote':{
                'book_title': book.title,
                'content': content
            }
        }), HTTP_201_CREATED
    
# read a specific quote
@user_quotes.route('/<int:quote_id>', methods=['POST', 'GET'])
@jwt_required()
def get_specific_quote(quote_id):
    quote = Quote.query.filter_by(id=quote_id).first()
    
    if not quote:
        return jsonify({'error': 'Quote not found.'}), HTTP_404_NOT_FOUND

    return jsonify(
        {
            'quote':{
                'id': quote.id,
                'book_title': quote.book.title,
                'content': quote.content,
                'created_at': quote.created_at
            }
        }
    ), HTTP_200_OK

# delete a specific post
@user_quotes.route('/delete/<int:quote_id>', methods=['DELETE'])
@jwt_required()
def delete_quote(quote_id):
    userId = get_jwt_identity()

    if not userId:
        return jsonify({'error': 'You are not allowed to delete this qoute.'}), HTTP_400_BAD_REQUEST
    
    quote = Quote.query.filter_by(id=quote_id, user_id=userId).first()
    
    if not quote:
        return jsonify({'error': 'Quote not available.'}), HTTP_404_NOT_FOUND

    if request.method == "DELETE":
        db.session.delete(quote)
        db.session.commit()

        return jsonify({'message': 'Quote deleted successfully!'}), HTTP_200_OK

