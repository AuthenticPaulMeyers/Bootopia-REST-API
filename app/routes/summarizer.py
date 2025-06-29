from flask import request, Blueprint, jsonify
from ..constants.http_status_codes import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK
from ..services.get_summary import summarize_section
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..schema.models import Book, Summary, db
from ..utils.limit_tokens_count import truncate_text_to_token_limit
from ..utils.downloads import download_or_get_local_file
from ..utils.get_text_from_pdf import extract_text_content
from app import limiter, get_remote_address

summarize = Blueprint('summaries', __name__, static_folder='static', url_prefix='/api/v1.0/summaries')

@summarize.route('/book/<int:book_id>/summarize', methods=['POST'])
@limiter.limit("10 per day", key_func=get_remote_address)
@jwt_required()
def summarise_book(book_id):
    user_id = get_jwt_identity()

    if request.method == 'POST':
        book = Book.query.filter_by(id=book_id).first()

        if not book:
            return jsonify({'error': 'Book not found.'}), HTTP_404_NOT_FOUND
        
        book_url = book.file_url

        try:
            file_path = download_or_get_local_file(book_url)
            text_content = extract_text_content(file_path)
            limited_text = truncate_text_to_token_limit(text_content, max_tokens=6000)

            summary_text = summarize_section(limited_text)

            if not summary_text or summary_text == '':
                return jsonify({'message': 'Summary is empty.'})

            summary = Summary(user_id=user_id, book_id=book.id, summary_text=summary_text)
            db.session.add(summary)
            db.session.commit()

            return jsonify({
                "summary":{
                    "status": "success",
                    "book": book.title,
                    "author": book.author,
                    "summary_text": summary_text
                }
            })
        
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), HTTP_500_INTERNAL_SERVER_ERROR

@summarize.route('/summary/<int:summary_id>')
@jwt_required()
def get_summarized_text(summary_id):
    user_id = get_jwt_identity()

    summary = Summary.query.filter_by(user_id=user_id, id=summary_id).first()

    if not summary:
        return jsonify({'error': 'Summary not found.'}), HTTP_404_NOT_FOUND
    
    return jsonify({
        'summary': {
            'book': summary.book.title,
            'author': summary.book.author,
            'summary_text': summary.summary_text
        }
    }), HTTP_200_OK

# List all summaries
@summarize.route('/summaries/<int:book_id>/all')
@jwt_required()
def get_all_summaries(book_id):
    
    summaries = Summary.query.filter_by(book_id=book_id).all()

    if not summaries:
        return jsonify({'error': 'No summaries found.'}), HTTP_404_NOT_FOUND
    
    summary_data = []

    for summary in summaries:
        summary_data.append({
            'book': summary.book.title,
            'author': summary.book.author,
            'summary_text': summary.summary_text
        })
    return ({'summaries': summary_data}), HTTP_200_OK

# delete a summary
@summarize.route('/summary/<int:summary_id>/delete', methods=['DELETE'])
@jwt_required()
def delete_summary(summary_id):
    user_id = get_jwt_identity()

    summary = Summary.query.filter_by(user_id=user_id, id=summary_id).first()

    if not summary:
        return jsonify({'error': 'Summary not found.'}), HTTP_404_NOT_FOUND
    
    db.session.delete(summary)
    db.session.commit()

    return jsonify({'message': 'Summary deleted successfully.'}), HTTP_200_OK

# Get all summaries for a user
@summarize.route('/', methods=['GET'])
@jwt_required()
def get_user_summaries():
    user_id = get_jwt_identity()

    summaries = Summary.query.filter_by(user_id=user_id).all()

    if not summaries:
        return jsonify({'error': 'No summaries found.'}), HTTP_404_NOT_FOUND

    summary_data = []

    for summary in summaries:
        summary_data.append({
            'book': summary.book.title,
            'author': summary.book.author,
            'summary_text': summary.summary_text
        })

    return jsonify({'summaries': summary_data}), HTTP_200_OK