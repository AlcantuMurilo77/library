from models.library import User, Library, Book
import random
import datetime
import db 
library = Library()
import utils
from flask import Flask, request, jsonify
from marshmallow import Schema, fields, validate, ValidationError

def register_user():
    try:
        data = request.get_json()

        user_schema = utils.UserSchema()
        try:
            user = user_schema.load(data)
        except ValidationError as err:
            return jsonify({"error": "Invalid data", "details": err.messages}), 400

        username = user.get('username')

        result = db.insert_user(username)

        return jsonify({"message": "User registered successfully"}), 200

    except Exception as e:
        return jsonify({"error": f"Unexpected error: {e}"}), 500
