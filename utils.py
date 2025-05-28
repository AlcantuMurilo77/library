import re
from marshmallow import Schema, fields, validate, ValidationError
from datetime import datetime

"""
Using Marshmallow:

Marshmallow is used in this project to validate and deserialize data received in HTTP requests.
It converts JSON-formatted data into Python objects, applying validation rules to ensure
the data is correct before being processed.

1. Schemas and Validation
   - Marshmallow uses schemas to define data structures and validations. In our code, we have three schemas:
     - BookSchema: Validates book data (title, author, and year). Title and author must be
     non-empty alphanumeric strings, and year must be in the range from 0 up to the current year.
     - UserSchema: Validates the username, which must be a non-empty alphanumeric string.
     - IDSchema: Validates that the ID is a positive integer.
   
2. Deserialization and Validation
   - The `load()` method of Marshmallow is used to load data (convert JSON to Python) and
   validate it according to the rules defined in the schemas.
   If the data is invalid, a `ValidationError` is raised, and the errors are returned in the response.

3. Example of usage:
   book_schema = utils.BookSchema()
   try:
       book = book_schema.load(data)   - Validates and loads the data
   except ValidationError as err:
       return jsonify({"error": "Invalid data", "details": err.messages}), 400
"""

current_year = datetime.now().year

def validate_alphanumeric(value):
    if not re.match("^[A-Za-z0-9 ]+$", value):
        raise ValidationError("The value contains invalid characters.")
    return value

def validate_id(value):
    if not value:
        raise ValidationError("The ID cannot be empty.")
    if not isinstance(value, int) or value <= 0:
        raise ValidationError("The ID must be a positive integer.")
    return value


class BookSchema(Schema):
    title = fields.String(required=True, validate=[
        validate.Length(min=1, error="The title cannot be empty."),
        validate_alphanumeric
    ])
    author = fields.String(required=True, validate=[
        validate.Length(min=1, error="The author cannot be empty."),
        validate_alphanumeric
    ])
    year = fields.Integer(required=True, validate=validate.Range(
        min=0, max=current_year, error="The year must be between 0 and the current year."
    ))

class UserSchema(Schema):
    username = fields.String(required=True, validate=[
        validate.Length(min=1, error="The username cannot be empty."),
        validate_alphanumeric
    ])

class IDSchema(Schema):
    id = fields.Integer(
        required=True,
        validate=[validate_id]
    )
