from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# initialise the database
db = SQLAlchemy()

# This file has 13 models

# Users table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False, unique=True)
    email = db.Column(db.String(90), nullable=False, unique=True)
    bio = db.Column(db.Text, nullable=True)
    password_hash = db.Column(db.Text, nullable=False)
    profile_pic_url = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    books = db.relationship('Book', backref='user', lazy=True)
    posts = db.relationship('Post', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)
    likes = db.relationship('Like', backref='user', lazy=True)
    followers = db.relationship('Follower', foreign_keys='Follower.following_id', backref='following', lazy=True)
    following = db.relationship('Follower', foreign_keys='Follower.follower_id', backref='follower', lazy=True)
    user_books = db.relationship('UserBook', backref='user', lazy=True)
    summaries = db.relationship('Summary', backref='user', lazy=True)
    quotes = db.relationship('Quote', backref='user', lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True)

    def __repr__(self) -> str:
        return f'User>>>{self.username}'

# Books table
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    cover_image_url = db.Column(db.Text)
    year_published = db.Column(db.Integer)
    isbn = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user_books = db.relationship('UserBook', backref='book', lazy=True)
    posts = db.relationship('Post', backref='book', lazy=True)
    summaries = db.relationship('Summary', backref='book', lazy=True)
    quotes = db.relationship('Quote', backref='book', lazy=True)
    tags = db.relationship('BookTag', backref='book', lazy=True)

    def __repr__(self) -> str:
        return f'Book>>>{self.id}'


# UserBook table to track the books the user is reading
class UserBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"))
    status = db.Column(db.String(20))
    personal_note = db.Column(db.Text)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'UserBook>>>{self.id}'

# Genre table
class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    books = db.relationship('Book', backref='genre', lazy=True)

    def __repr__(self) -> str:
        return f'Genre>>>{self.id}'


# Posts table
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"))
    content = db.Column(db.Text, nullable=False)
    post_image_url = db.Column(db.Text, nullable=True)
    posted_at = db.Column(db.DateTime, default=datetime.utcnow)
    comments = db.relationship('Comment', backref='post', lazy=True)
    likes = db.relationship('Like', backref='post', lazy=True)

    def __repr__(self) -> str:
        return f'Post>>>{self.id}'


# Comments table
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
    comment = db.Column(db.Text, nullable=False)
    posted_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'Comment>>>{self.id}'

# Likes table
class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'Like>>>{self.id}'

# Followers table
class Follower(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    following_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    followed_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'Follower>>>{self.id}'

# Summaries table to store AI generated summaries
class Summary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"))
    summary_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'Summary>>>{self.id}'

# Quotes table to store user saved quotes
class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"))
    quote = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'Quote>>>{self.id}'

# Tags table
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    book_tags = db.relationship('BookTag', backref='tag_obj', lazy=True)

    def __repr__(self) -> str:
        return f'Tag>>>{self.id}'

# BookTags table
class BookTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"))
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'BookTag>>>{self.id}'

# Notifications table
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'Notification>>>{self.id}'
