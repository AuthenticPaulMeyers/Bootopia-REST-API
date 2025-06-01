from flask import Blueprint, request, url_for, redirect, jsonify
from ..schema.models import db, Book
from flask_jwt_extended import jwt_required
from ..constants.http_status_codes import HTTP_200_OK

books = Blueprint("books", __name__, static_url_path="static/", url_prefix="/books")

# Add new book route
@books.route("/", methods=['POST', 'GET'])
def get_all_books():

    # add pagination
    page=request.args.get('page', 1, type=int)
    per_page=request.args.get('per_page', 10, type=int)

    # List all the books with pagination and sort
    books = Book.query.all().paginate(page=page, per_page=per_page)
    data = []
        
    if books:
        for book in books.items:
            data.append(
                {
                    'id': book.id,
                    'title': book.title,
                    'author': book.author,
                    'description': book.description,
                    'genre': book.genre.name,
                    'cover_image_url': book.cover_image_url,
                    'year_published': book.year_published,
                    'isbn': book.isbn
                    }
                )
        metadata={
            'page': books.page,
            'per_page':books.per_page,
            'has_next': books.has_next,
            'has_prev': books.has_prev,
            'total': books.total,
            'next_page': books.next_num,
            'prev_page': books.prev_num
        }
        return jsonify({'data': data, 'metadata': metadata}), HTTP_200_OK
    return {'message': 'No books currently available!'}

# Updated book route
@books.route("/update/<int:book_id>")
@jwt_required()
def update_book():
    return 

# Get a specific book
@books.route("/<int:book_id>")
@jwt_required()
def get_book():
    return

# Search books
@books.route("/search")
@jwt_required()
def search_books():
    return
