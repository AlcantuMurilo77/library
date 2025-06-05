from models.library import User, Library, Book
import random
import datetime
import db 
users = []
library = Library()
import utils
from flask import jsonify, request, Response
from marshmallow import ValidationError

def add_book():
    try:
        data = request.get_json()

        book_schema = utils.BookSchema()
        try:
            book = book_schema.load(data)
        except ValidationError as err:
            return jsonify({"error": "Invalid data", "details": err.messages}), 400

        title = book.get('title')
        author = book.get('author')
        year = book.get('year')
        
        result = db.insert_book(title, author, year, available=1)
        return jsonify({"message": "Book added successfully!"}), 200
    
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {e}"}), 500
    

def delete_book():
    try:
        data = request.get_json()
        id_schema = utils.IDSchema()

        try:
            book_id = id_schema.load(data)
        except ValidationError as err:
            return jsonify({"error": "Invalid data", "details": err.messages}), 400
        
        book_id = book_id.get("id")
        result = db.delete_book(book_id)
        return result, 201
    
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {e}"}), 500


def search_book():
    try:
        data = request.get_json()
        id_schema = utils.IDSchema()

        try:
            book_id = id_schema.load(data)
        except ValidationError as err:
            return jsonify({"error": "Invalid data", "details": err.messages}), 400
        
        book_id = book_id.get("id")
        result = db.get_book_by_id(book_id)
        
        if result is None:
            return jsonify({"error": "Book not found"}), 404
        
        return result, 200
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {e}"}), 500


def borrow_book():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Missing or invalid JSON body"}), 400

        id_schema = utils.IDSchema()
        try:
            user_id = id_schema.load({"id": data.get("user_id")})
        except ValidationError as err:
            return jsonify({"error": "Invalid user ID", "details": err.messages}), 400

        user_id = user_id.get("id")

        try:
            book_id = id_schema.load({"id": data.get("book_id")})
        except ValidationError as err:
            return jsonify({"error": "Invalid book ID", "details": err.messages}), 400

        book_id = book_id.get("id")

        if db.get_user_by_id(user_id) is None:
            return jsonify({"error": "User not found"}), 404
        
        if db.get_book_by_id(book_id) is None:
            return jsonify({"error": "Book not found"}), 404

        if not db.check_book_availability(book_id):
            return jsonify({"error": "Book is not available for borrowing"}), 409
        
        return(db.insert_loan(book_id, user_id))

        
    except Exception as e:

        return jsonify({"error": f"Unexpected error: {e}"}), 500
    

def return_book():
    try:
        data = request.get_json()
        id_schema = utils.IDSchema()

        try:
            user_id = id_schema.load({"id": data.get("user_id")})
        except ValidationError as err:
            return jsonify({"error": "Invalid user ID", "details": err.messages}), 400
        
        user_id = user_id.get("id")

        try:
            book_id = id_schema.load({"id": data.get("book_id")})
        except ValidationError as err:
            return jsonify({"error": "Invalid book ID", "details": err.messages}), 400
        
        book_id = book_id.get("id")

        if db.find_user_by_id(user_id) is None:
            return jsonify({"error": "User not found"}), 404

        book_data = db.get_book_by_id(book_id)
        if isinstance(book_data, Response):
            book_data = book_data.get_json()

        if book_data is None:
            return jsonify({"error": "Book not found"}), 404

        user_borrows = db.find_user_pending_borrows(user_id)
        matched = None
        for borrow in user_borrows:
            if book_data['title'].lower() == borrow['book_title'].lower():
                matched = borrow['book_title'].lower()

        if matched is None:
            return jsonify({"error": "Book was not borrowed by this user or has already been returned."}), 409

        db.mark_book_returned(user_id, book_id)
        result = db.set_book_available(book_id)
        return result, 201

    except Exception as e:
        return jsonify({"error": f"Unexpected error: {e}"}), 500


def list_user_borrowed_books():
    try:
        data = request.get_json()
        id_schema = utils.IDSchema()
        
        try:
            user_id = id_schema.load(data)
        except ValidationError as err:
            return jsonify({"error": "Invalid data", "details": err.messages}), 400

        user_id = user_id.get("id")

        if db.find_user_by_id(user_id) is None:
            return jsonify({"error": "User not found"}), 404

        result = db.find_user_pending_borrows(user_id)
        if not result:
            return jsonify([]), 200
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {e}"}), 500
