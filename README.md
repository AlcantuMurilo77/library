# Library Management System

This is a simple Library Management System built with **Flask**, **Python**, and **SQL**. The application provides core functionalities such as adding, deleting, and listing books, user registration, and data validation to ensure data integrity.

---

## Features

- **Book Management**  
  Add, delete, and list books in the library.

- **User Management**  
  Register and manage users.

- **Data Validation**  
  Data validation is handled using Marshmallow to ensure accuracy and provide informative error messages.

- **RESTful API**  
  The system follows REST principles using Flask for clean and structured API development.

- **Database Integration**  
  All data is stored and managed in a SQL database. Validation is enforced before insertion.

---

## Technologies Used

| Technology   | Description                                                 |
|--------------|-------------------------------------------------------------|
| Flask        | Lightweight Python web framework used to build the API     |
| SQL          | Used for data storage and relational database operations    |
| Marshmallow  | Used for data serialization and validation                  |
| Python       | Primary language for backend logic                          |
| Jinja2       | Flask’s templating engine for dynamic HTML (if needed)      |
| HTML         | Basic markup for user interface                             |
| CSS          | Styles the user interface for better usability              |
| JavaScript   | Adds interactivity to the UI                                |

---

## Skills Developed

- **Flask Framework**  
  Built RESTful APIs, handled routing, requests, and responses.

- **SQL Database Management**  
  Interacted with relational databases, created queries, and ensured data consistency.

- **Data Validation with Marshmallow**  
  Implemented input validation and custom error messaging.

- **Problem Solving**  
  Handled data consistency, debugged issues, and managed user input errors.

- **API Development**  
  Gained experience with HTTP methods like GET, POST, and DELETE.

- **Web Development**  
  Worked with HTML, CSS, and JavaScript for basic UI design and interaction.

- **Version Control with GitHub**  
  Used Git and GitHub for source control and project management.

---

## How It Works

The system exposes a RESTful API to manage a collection of books. Each book has attributes like title, author, and year. Registered users can access the system, and an administrator can manage the library content. All incoming data is validated before being stored in the database.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/library-management-system.git
   cd library-management-system
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/macOS
   venv\Scripts\activate     # For Windows
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   flask run
   ```

---
