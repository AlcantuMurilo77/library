import services
import services.book_services
import services.user_services
import db
from flask_cors import CORS
from flask import Flask, jsonify

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}})

@app.route("/listbooks", methods=['GET']) 
def list_books():
    books = db.get_books()
    return jsonify(books)

@app.route("/addbook", methods=['POST']) 
def add_book():
    services.book_services.add_book()
    return jsonify({"message": "Book added successfully!"})

@app.route("/listusers", methods=['GET']) 
def list_users():
    users = db.get_users()
    return jsonify(users)

@app.route("/adduser", methods=['POST']) 
def add_user():
    return services.user_services.register_user()

@app.route("/borrowedbooksbyuser", methods=['POST'])
def list_borrowed_books():
    return services.book_services.list_user_borrowed_books()

@app.route("/borrowbook", methods=["POST"])
def borrow_book():
    return services.book_services.borrow_book()

@app.route("/returnbook", methods=['POST']) 
def return_book():
    return services.book_services.return_book()

@app.route("/searchbook", methods=['POST']) 
def search_book():
    return services.book_services.search_book()

@app.route("/deletebook", methods=["DELETE"]) 
def delete_book():
    return services.book_services.delete_book()

if __name__ == '__main__':
    app.run()
