import db
from db import con
from mysql.connector import Error

class Book:
    title: str
    author: str
    year: int
    id: int

    def __init__(self, title, author, year, id, available):
        self.title = title
        self.author = author
        self.year = year
        self.id = id
        self.available = available
    
    def borrow(self):
        self.available = False

    def return_book(self):
        self.available = True
    
    def show_availability(self):
        return "Available" if self.available else "Not available"
    
    def __repr__(self):
        return f"<Book {self.title}, Author {self.author}, Published in {self.year}, Availability: {self.show_availability()}>"

class User:
    name: str

    def __init__(self, name, id):
        self.name = name
        self.borrowed_books = []
        self.id = id

    def borrow_book(self, book):
        if book.available:
            self.borrowed_books.append(book)
            book.borrow()
    
    def return_book(self, book):
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)
            book.return_book()

class Library:
    def __init__(self):
        self.catalog = []
    
    def add_book(self, book):
        self.catalog.append(book)

    def search_book(self, title):
        found = False
        for book in self.catalog:
            if book.title.upper() == title.upper():
                print(f"Book found: Title: {book.title} | Author: {book.author} | Year: {book.year} | Availability: {book.show_availability()} | ID: {book.id}")
                found = True
                break

    def list_available_books(self):
        print("Available books:\n")
        for book in self.catalog:
            if book.available:
                print(f"- {book}\n")
