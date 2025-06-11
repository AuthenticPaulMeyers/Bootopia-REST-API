from flask import request, Blueprint, jsonify
from ..schema.models import db, Post, Book, Likes, Comment
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..constants.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from ..utils.image_upload import upload_image

# create a blueprint for this route
user_posts = Blueprint('posts', __name__, static_url_path='static/', url_prefix='/posts')

# get all posts
@user_posts.route('/')
@jwt_required()
def posts():
    posts = Post.query.all()

    if not posts:
        return jsonify({'message': 'No posts currently available!'}), HTTP_204_NO_CONTENT

    posts_data = []
    for post in posts:
        likes_count = Likes.query.filter_by(post_id=post.id).count()
        comments = Comment.query.filter_by(post_id=post.id).all()
        comments_data = [
            {
                'id': comment.id,
                'user': comment.users.username,
                'content': comment.content,
                'date_posted': comment.posted_at
            }
            for comment in comments
        ]
        posts_data.append({
            'id': post.id,
            'user': post.users.username,
            'title': post.title,
            'book': post.book.title,
            'content': post.content,
            'post_image_url': post.post_image_url,
            'likes': likes_count,
            'date_posted': post.posted_at,
            'comments': comments_data
            
        })
    return jsonify({'posts': posts_data}), HTTP_200_OK

# get user posts
@user_posts.route('/user/<int:user_id>')
@jwt_required()
def get_posts_from_single_user(user_id):

    posts = Post.query.filter_by(user_id=user_id).all()

    if not posts:
        return jsonify({'message': 'No posts currently available!'}), HTTP_204_NO_CONTENT

    posts_data = []
    for post in posts:
        likes_count = Like.query.filter_by(post_id=post.id).count()
        comments = Comment.query.filter_by(post_id=post.id).all()
        comments_data = [
            {
                'id': comment.id,
                'user': comment.users.username,
                'content': comment.content,
                'date_posted': comment.posted_at
            }
            for comment in comments
        ]
        posts_data.append({
            'id': post.id,
            'user': post.users.username,
            'title': post.title,
            'book': post.book.title,
            'content': post.content,
            'post_image_url': post.post_image_url,
            'likes': likes_count,
            'date_posted': post.posted_at,
            'comments': comments_data
            
        })

    return jsonify({'posts': posts_data}), HTTP_200_OK

# create a posts
@user_posts.route('/new', methods=['POST', 'GET'])
@jwt_required()
def create_post():
    userId = get_jwt_identity()

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        book_title = request.form.get('book_title')
        post_image = request.files['post_image']

        if not (title and content and book_title):
            return jsonify({'error': 'Missing required fields.'}), HTTP_400_BAD_REQUEST
        
        if not post_image:
            return jsonify({'error': 'No file selected.'}), HTTP_400_BAD_REQUEST
        
        # get the book ID
        book = Book.query.filter_by(title=book_title).first()
        if not book:
            return jsonify({'error': 'Book not found.'}), HTTP_404_NOT_FOUND
        
        book_id = book.id
        
        post_image_url = upload_image(post_image)
        if not post_image_url:
            return ({'error': 'Invalid file type.'}), HTTP_400_BAD_REQUEST

        post = Post(
            title=title,
            content=content,
            user_id=userId,
            book_id=book_id,
            post_image_url=post_image_url
        )
        db.session.add(post)
        db.session.commit()

        return jsonify({
            'message': 'Post added successfully!',
            'post':{
                'title': title,
                'content': content,
                'book_title': book_title,
                'post_image_url': post_image_url
            }
        }), HTTP_201_CREATED
    
# get a specific post
@user_posts.route('/<int:post_id>', methods=['POST', 'GET'])
@jwt_required()
def get_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    
    if not post:
        return jsonify({'error': 'Post not found.'}), HTTP_404_NOT_FOUND
        
    likes_count = Like.query.filter_by(post_id=post.id).count()
    comments = Comment.query.filter_by(post_id=post.id).all()

    if not comments:
        return jsonify({'message': 'No comments currently available.'}), HTTP_204_NO_CONTENT
    
    comments_data = [
        {
            'id': comment.id,
            'user': comment.users.username,
            'content': comment.content,
            'date_posted': comment.posted_at
        }
        for comment in comments
    ]

    return jsonify(
        {
            'id': post.id,
            'user': post.users.username,
            'title': post.title,
            'book': post.book.title,
            'content': post.content,
            'post_image_url': post.post_image_url,
            'likes': likes_count,
            'date_posted': post.posted_at,
            'comments': comments_data
        }
    ), HTTP_200_OK

# update a specific post
@user_posts.route('/edit/<int:post_id>', methods=['PUT', 'GET'])
@jwt_required()
def update_post(post_id):
    userId=get_jwt_identity()
    
    post=Post.query.filter_by(id=post_id, user_id=userId).first()
    
    if request.method == 'PUT':
        if post:
            title = request.form.get('title')
            content = request.form.get('content')
            book_title = request.form.get('book_title')
            post_image = request.files['post_image']

            if not (title and content and book_title):
                return jsonify({'error': 'Missing required fields.'}), HTTP_400_BAD_REQUEST
            
            if not post_image:
                return jsonify({'error': 'No file selected.'}), HTTP_400_BAD_REQUEST

            # get the book ID
            book = Book.query.filter_by(title=book_title).first()
            if not book:
                return jsonify({'error': 'Book not found.'}), HTTP_404_NOT_FOUND
            
            book_id = book.id
        
            post_image_url = upload_image(post_image)
            if not post_image_url:
                return ({'error': 'Invalid file type.'}), HTTP_400_BAD_REQUEST
            
            post.title = title
            post.content = content
            post.user_id = userId
            book.book_id = book_id
            book.post_image_url = post_image_url
            db.session.commit()

            return jsonify({
            'message': 'Post added successfully!',
            'post':{
                'title': post.title,
                'content': post.content,
                'book_title': post.book.title,
                'post_image_url': post.post_image_url
                }
            }), HTTP_201_CREATED
        else:
            return jsonify({'error': f'{HTTP_400_BAD_REQUEST} Bad request'}), HTTP_400_BAD_REQUEST

# delete a specific post
@user_posts.route('/delete/<int:post_id>', methods=['DELETE', 'GET'])
@jwt_required()
def delete_post(post_id):
    userId = get_jwt_identity()

    if not userId:
        return jsonify({'error': 'You are not allowed to delete this post.'}), HTTP_400_BAD_REQUEST
    
    post = Post.query.filter_by(id=post_id, user_id=userId).first()
    
    if not post:
        return jsonify({'error': 'Post not available.'}), HTTP_404_NOT_FOUND
    db.session.delete(post)
    db.session.commit()

    return jsonify({'message': 'Post deleted!'}), HTTP_200_OK

