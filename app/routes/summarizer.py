from flask import request, Blueprint, jsonify
from ..constants.http_status_codes import HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR
from ..services.get_summary import summarize_section, MODEL
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..schema.models import Book, Summary, db
import os
from ..utils.limit_tokens_count import truncate_text_to_token_limit
from ..utils.downloads import download_or_get_local_file
from ..utils.get_text_from_pdf import extract_text_content

summarize = Blueprint('summarize', __name__, static_folder='static', url_prefix='/summarize')

@summarize.route('/book/<int:book_id>', methods=['POST'])
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
