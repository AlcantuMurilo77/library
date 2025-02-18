Library Management System


This is a simple Library Management System built using Flask, Python, and SQL. The application provides basic functionalities such as adding, deleting, and listing books. It allows for basic user management and integrates a validation system to ensure data integrity.

Key Features


Book Management: Add, delete, and list books in the library.

User Management: Register and manage users.

Data Validation: Implemented using Marshmallow to ensure data integrity and provide meaningful error messages.

RESTful API: The system is built as a RESTful API using Flask, following best practices for API development.
Database Integration: The system uses SQL to store and manage data. All data is validated before being inserted into the database.
Technologies Used

Flask: A lightweight Python web framework used to build the API.

SQL: Structured Query Language for interacting with the database.

Marshmallow: Used for data serialization and validation, ensuring that only valid data is processed.

Python: The primary language used for developing the application.

Jinja2: Templating engine used by Flask to dynamically generate HTML (if required).

HTML: Used for structuring the basic user interface for displaying book data and interacting with the system.

CSS: Employed for styling the user interface, making the application visually appealing and user-friendly.

JavaScript: Utilized for adding basic interactivity to the application, such as handling user input and updating the UI dynamically.
Skills Developed
Throughout the development of this project, I gained hands-on experience with the following skills:

Flask Framework: Built a RESTful API with Flask, managing routing, handling requests, and structuring responses.
Database Management with SQL: Learned how to interact with relational databases, write SQL queries, and manage data integrity.
Data Validation with Marshmallow: Used Marshmallow to implement data validation for user inputs and to create clear error messages when validation fails.

Problem Solving: Encountered various challenges during development, such as handling user inputs, ensuring data consistency, and troubleshooting bugs.

API Development: Gained practical experience in creating APIs that interact with databases and handle various types of requests (GET, POST, DELETE).

Web Development: Gained experience in basic HTML for structuring the user interface, CSS for styling, and JavaScript for adding interactivity.

GitHub for Version Control: Utilized GitHub for version control, ensuring proper collaboration and tracking of changes throughout the development process.

How It Works
The system is designed to manage a library of books, with an API to handle book and user management. Each book is stored in the database with attributes like title, author, and year of release. Users can register to access the system, and the administrator can manage the books in the library. The API validates all incoming data to ensure correctness and consistency.
