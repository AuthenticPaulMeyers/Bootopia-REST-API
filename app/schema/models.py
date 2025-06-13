from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
# initialise the database
db = SQLAlchemy()

# This file has 12 models

# Users table
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False, unique=True)
    email = db.Column(db.String(90), nullable=False, unique=True)
    bio = db.Column(db.Text, nullable=True)
    password_hash = db.Column(db.Text, nullable=False)
    profile_pic_url = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    books = db.relationship('Book', backref='users', lazy=True)
    posts = db.relationship('Post', backref='users', lazy=True)
    comments = db.relationship('Comment', backref='users', lazy=True)
    likes = db.relationship('Likes', backref='users', lazy=True)
    followers = db.relationship('Follower', foreign_keys='Follower.following_id', backref='following', lazy=True)
    following = db.relationship('Follower', foreign_keys='Follower.follower_id', backref='follower', lazy=True)
    user_books = db.relationship('UserBook', backref='users', lazy=True)
    summaries = db.relationship('Summary', backref='users', lazy=True)
    quotes = db.relationship('Quote', backref='users', lazy=True)
    notifications = db.relationship('Notification', backref='users', lazy=True)
    user_moods = db.relationship('UserMood', backref='users', lazy=True)
    user_recommendations = db.relationship('UserRecommendation', backref='users', lazy=True)

    def __repr__(self) -> str:
        return f'Users>>>{self.id}'

# Books table
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, unique=True)
    author = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    cover_image_url = db.Column(db.Text)
    file_url = db.Column(db.Text)
    year_published = db.Column(db.Integer)
    isbn = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user_books = db.relationship('UserBook', backref='book', lazy=True)
    posts = db.relationship('Post', backref='book', lazy=True)
    summaries = db.relationship('Summary', backref='book', lazy=True)
    quotes = db.relationship('Quote', backref='book', lazy=True)
    tags = db.relationship('BookTag', backref='book', lazy=True)
    user_recommendations = db.relationship('UserRecommendation', backref='book', lazy=True)
    book_moods = db.relationship('BookMood', backref='book', lazy=True)

    def __repr__(self) -> str:
        return f'Book>>>{self.id}'

# UserBook/Bookmark/Favourites/Reading list table to track the books the user is reading
class UserBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"))
    status = db.Column(db.String(20), default='want_to_read')
    personal_note = db.Column(db.Text)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'UserBook>>>{self.id}'

# Posts table
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"))
    content = db.Column(db.Text, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    post_image_url = db.Column(db.Text, nullable=True)
    posted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    comments = db.relationship('Comment', backref='post', lazy=True)
    likes = db.relationship('Likes', backref='post', lazy=True)
    posst_moods = db.relationship('PostMood', backref='post', lazy=True)

    def __repr__(self) -> str:
        return f'Post>>>{self.id}'
    
    def to_dict(self, user_id=None):
        return {
            'id': self.id,
            'posted_by': self.users.username,
            'content': self.content,
            'title': self.title,
            'post_image_url': self.post_image_url,
            'posted_at': self.posted_at.isoformat(),
            'book_title': self.book.title,
        }


# Comments table
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
    content = db.Column(db.Text, nullable=False)
    posted_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'Comment>>>{self.id}'

# Likess table
class Likes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'Likes>>>{self.id}'

# Followers table
class Follower(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    following_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    followed_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'Follower>>>{self.id}'

# Summaries table to store AI generated summaries
class Summary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"))
    summary_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'Summary>>>{self.id}'

# Quotes table to store user saved quotes
class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))
    book_id = db.Column(db.Integer, db.ForeignKey("book.id", ondelete="CASCADE"))
    quote = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'Quote>>>{self.id}'

# Tags table
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
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
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'Notification>>>{self.id}'
    
# Moods table
class Mood(db.Model):
    __tablename__ = "moods"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)
    user_moods = db.relationship('UserMood', backref='mood', lazy=True)
    post_moods = db.relationship('PostMood', backref='mood', lazy=True)
    book_moods = db.relationship('BookMood', backref='mood', lazy=True)

    def __repr__(self) -> str:
        return f'Mood>>>{self.id}'

# User mapping to moods table
class UserMood(db.Model):
    __tablename__ = "user_moods"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), index=True)
    mood_id = db.Column(db.ForeignKey("moods.id", ondelete="CASCADE"), index=True)
    strength = db.Column(db.SmallInteger, default=1)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self) -> str:
        return f'UserMood>>>{self.id}'

# book mapping to mood
class BookMood(db.Model):
    __tablename__ = "book_moods"
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.ForeignKey("book.id", ondelete="CASCADE"), index=True)
    mood_id = db.Column(db.ForeignKey("moods.id", ondelete="CASCADE"), index=True)

    def __repr__(self) -> str:
        return f'BookMood>>>{self.id}'

# Post mood table | mapping posts with moods
class PostMood(db.Model):
    __tablename__ = "post_moods"
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.ForeignKey("post.id", ondelete="CASCADE"), index=True)
    mood_id = db.Column(db.ForeignKey("moods.id", ondelete="CASCADE"), index=True)

    def __repr__(self) -> str:
        return f'PostMood>>>{self.id}'

# Recommendations with matching moods
class UserRecommendation(db.Model):
    __tablename__ = "user_recommendations"
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.ForeignKey("book.id", ondelete="CASCADE"), index=True)
    user_id = db.Column(db.ForeignKey("users.id", ondelete="CASCADE"), index=True)

    def __repr__(self) -> str:
        return f'UserRecommendation>>>{self.id}'

