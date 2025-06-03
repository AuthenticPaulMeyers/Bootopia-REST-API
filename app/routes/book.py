from flask import Blueprint, request, jsonify
from ..schema.models import db, Book, Genre
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..constants.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_201_CREATED
from ..utils.file_upload import upload_file
from ..utils.image_upload import upload_image

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
        cover_url = upload_image(cover)
        
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
        }), HTTP_201_CREATED
    
# Get a specific book
@books.route("/get/<int:book_id>")
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
    return jsonify({'error': 'Book not found.'}), HTTP_404_NOT_FOUND
    
# Search books
@books.route("/search")
@jwt_required()
def search_books():
    # implement a book search where users can search books based on the title or genre
    title = request.args.get('title')
    genre = request.args.get('genre')
    author = request.args.get('author')

    # get user id
    userId = get_jwt_identity()

    query = Book.query.filter_by(user_id=userId)

    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))
    if genre:
        query = query.join(Genre).filter(Genre.name.ilike(f"%{genre}%"))
    if author:
        query = query.filter(Book.author.ilike(f"%{author}%"))

    books = query.all()
    search_result_count = len(books)

    if not books:
        return jsonify({'message': 'No books found matching the criteria.'}), HTTP_404_NOT_FOUND

    data = []
    for book in books:
        data.append({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'description': book.description,
            'genre': book.genre.name,
            'cover_image_url': book.cover_image_url,
            'year_published': book.year_published,
            'isbn': book.isbn
        })

    return jsonify({
        'results_count': search_result_count,
        'books': data
        }), HTTP_200_OK

# Updated book route
@books.route("/update/<int:book_id>", methods=['PUT', 'GET'])
@jwt_required()
def update_book(book_id):
    userId=get_jwt_identity()
    
    book=Book.query.filter_by(id=book_id, user_id=userId).first()
    
    if request.method == 'PUT':
        if book:
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
            cover_url = upload_image(cover)
            
            if not file_url or not cover_url:
                return jsonify({'error': 'Invalid file type.'}), HTTP_400_BAD_REQUEST

            # Check if the genre already exists, if not, add it and get the id
            get_genre = Genre.query.filter_by(name=genre_name).first()
            if not get_genre:
                new_genre = Genre(name=genre_name)
                db.session.add(new_genre)
                db.session.commit()
                get_genre = new_genre
            
            book.title = title
            book.author = author
            book.description = description
            book.year_published = year_published
            book.isbn = isbn
            book.genre_id = get_genre.id
            book.file_url = file_url
            book.cover_image_url = cover_url
            db.session.commit()

            return jsonify({
                'id': book.id,
                'title': book.title,
                'description': book.description,
                'author': book.author,
                'isbn': book.isbn,
                'genre': book.genre.name,
                'year_published': book.year_published,
                'file_url': book.file_url,
                'cover_url': book.cover_image_url
                # 'updated_at': book.created_at
            }), HTTP_201_CREATED
        else:
            return jsonify({'error': f'{HTTP_400_BAD_REQUEST} Bad request'}), HTTP_400_BAD_REQUEST

# Delete a book
@books.route("/delete/<int:book_id>", methods=['DELETE'])
@jwt_required()
def delete_book(book_id):
    # get user id
    userId = get_jwt_identity()

    if request.method == 'DELETE':
        book = Book.query.filter_by(user_id=userId, id=book_id).first()
        if not book:
            return jsonify({'error': 'Book not found.'}), HTTP_404_NOT_FOUND

        db.session.delete(book)
        db.session.commit()
        return jsonify({'message': 'Book deleted successfully.'}), HTTP_200_OK
