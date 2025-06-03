from flask import Blueprint, request, url_for, redirect, jsonify
from ..schema.models import db, Book, Genre
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..constants.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_302_FOUND
from ..utils.file_upload import upload_file

books = Blueprint("books", __name__, static_url_path="static/", url_prefix="/books")

# Get books route
@books.route("/", methods=['POST', 'GET'])
def get_all_books():

    # add pagination
    page=request.args.get('page', 1, type=int)
    per_page=request.args.get('per_page', 10, type=int)

    # List all the books with pagination
    books = Book.query.paginate(page=page, per_page=per_page)
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

# Add new book route
@books.route("/add_new", methods=['POST', 'GET'])
@jwt_required()
def add_new_book():
    userId = get_jwt_identity()

    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        description = request.form.get('description')
        genre_name = request.form.get('genre_name')
        year_published = request.form.get('year_published')
        isbn = request.form.get('isbn')
        cover = request.files.get('cover')
        file = request.files.get('file')

        if title == '' or author == '' or genre_name == '':
            return jsonify({'error': 'Required fields cannot be null.'}), HTTP_400_BAD_REQUEST
        
        if not genre_name:
            return jsonify({'error': 'Required fields cannot be null.'}), HTTP_400_BAD_REQUEST
            

        if not file or not cover:
            return jsonify({'error': 'No file provided.'}), HTTP_400_BAD_REQUEST
        
        file_url = upload_file(file)
        cover_url = upload_file(cover)
        
        if not file_url or not cover_url:
            return jsonify({'error': 'Invalid file type.'}), HTTP_400_BAD_REQUEST
        
        # Check if the genre already exists, if not, add it and get the id
        get_genre = Genre.query.filter_by(name=genre_name).first()
        if not get_genre:
            new_genre = Genre(name=genre_name)
            db.session.add(new_genre)
            db.session.commit()
            get_genre = new_genre
        
        book = Book(title=title, author=author, description=description, genre_id=get_genre.id, isbn=isbn, year_published=year_published, cover_image_url=cover_url, file_url=file_url, user_id=userId)
        db.session.add(book)
        db.session.commit()

        return jsonify({
            'message': 'Book added successfully.',
            'book':{
                'title': title,
                'author': author,
                'description': description,
                'genre': genre_name,
                'isbn': isbn,
                'year_published': year_published,
                'cover_image_url': cover_url,
                'file_url': file_url
            }
        }), HTTP_200_OK
    
# Get a specific book
@books.route("/<int:book_id>")
@jwt_required()
def get_book(book_id):

    # get user id
    userId = get_jwt_identity()

    book = Book.query.filter_by(user_id=userId, id=book_id).first()

    if book:
        return jsonify({
            'book':{
                'id': book.id,
                'author': book.author,
                'title': book.title,
                'genre': book.genre.name,
                'description': book.description,
                'cover_url': book.cover_image_url,
                'file_url': book.file_url,
                'isbn': book.isbn,
                'year_published': book.year_published
            }
        }), HTTP_200_OK
    return jsonify({'error': 'File not found.'}), HTTP_404_NOT_FOUND
    
# Search books
@books.route("/search")
@jwt_required()
def search_books():
    return

# Updated book route
@books.route("/update/<int:book_id>")
@jwt_required()
def update_book(book_id):
    return 
