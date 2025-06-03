import sqlite3
from sqlite3 import Error
import models.library as library
from datetime import timedelta, date
from flask import jsonify, Response

DB_PATH = 'biblioteca.db'  

def connect_db():
    try:
        con = sqlite3.connect(DB_PATH)
        con.row_factory = sqlite3.Row
        return con
    except Error as e:
        print(f"Failed to connect to the database: {e}")
        return None

def insert_user(nome_usuario):
    try:
        con = connect_db()
        with con:
            insert_query = "INSERT INTO usuario (nome_usuario) VALUES (?)"
            con.execute(insert_query, (nome_usuario,))
    except Error as e:
        raise Exception(f"Failed to insert user: {e}")
    finally:
        if con:
            con.close()

def insert_book(title, author, year, available=1):
    try:
        con = connect_db()
        with con:
            insert_query = """INSERT INTO livro (titulo_livro, autor_livro, ano_livro, disponivel_livro) VALUES (?, ?, ?, ?)"""
            con.execute(insert_query, (title, author, year, available))
        return {"message": "Book successfully added!"}
    except Error as e:
        return {"error": f"Failed to insert book: {e}"}
    finally:
        if con:
            con.close()

def make_book_available(book_id):
    try:
        con = connect_db()
        with con:
            query = "UPDATE livro SET disponivel_livro = 1 WHERE id_livro = ?"
            con.execute(query, (book_id,))
        return jsonify({"message": "Book successfully returned!"})
    except Error as e:
        print(f"Error making book available: {e}")
        return
    finally:
        if con:
            con.close()

def insert_loan(book_id, user_id):
    try:
        today = date.today()
        due_date = today + timedelta(days=15)
        con = connect_db()
        with con:
            insert_query = """INSERT INTO emprestimo (id_usuario, id_livro, data_emprestimo, data_devolucao) VALUES (?, ?, ?, ?)"""
            con.execute(insert_query, (user_id, book_id, today.isoformat(), due_date.isoformat()))

            update_query = """UPDATE livro SET disponivel_livro = 0 WHERE id_livro = ?"""
            con.execute(update_query, (book_id,))
        return jsonify({"message": "Loan successfully registered!"})
    except Error as e:
        print("Failed to insert data into the DB: ", e)
        return
    finally:
        if con:
            con.close()

def get_users():
    users = []
    try:
        con = connect_db()
        with con:
            query = 'SELECT * FROM usuario'
            cursor = con.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                users.append({"id": row["id_usuario"], "name": row["nome_usuario"]})
        return users
    except Error as e:
        print(f"Failed to query the table: {e}")
        return Exception("Database error: " + str(e))
    finally:
        if con:
            con.close()

def get_user_by_id(user_id: int):
    try:
        con = connect_db()
        with con:
            query = 'SELECT * FROM usuario WHERE id_usuario = ?'
            cursor = con.execute(query, (user_id,))
            row = cursor.fetchone()
            if row:
                return library.Usuario(nome=row["nome_usuario"], id=row["id_usuario"])
            else:
                return None
    except Error as e:
        return jsonify({"error": f"Error fetching user: {e}"})
    finally:
        if con:
            con.close()

def get_books():
    books = []
    try:
        con = connect_db()
        with con:
            query = 'SELECT * FROM livro'
            cursor = con.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                book = {
                    "id": row["id_livro"],
                    "title": row["titulo_livro"],
                    "author": row["autor_livro"],
                    "year": row["ano_livro"],
                    "available": "Available" if row["disponivel_livro"] else "Unavailable"
                }
                books.append(book)
        return books
    except Error as e:
        print(f"Failed to query the table: {e}")
        return
    finally:
        if con:
            con.close()

def get_book_by_id(book_id):
    try:
        con = connect_db()
        with con:
            query = 'SELECT * FROM livro WHERE id_livro = ?'
            cursor = con.execute(query, (book_id,))
            row = cursor.fetchone()
            if not row:
                return None
            book = library.Livro(row["titulo_livro"], row["autor_livro"], row["ano_livro"], row["id_livro"], disponivel=row["disponivel_livro"])
            return jsonify({
                "id": book.id,
                "title": book.titulo,
                "author": book.autor,
                "year": book.ano,
                "available": book.disponivel
            })
    except Error as e:
        print(f"Database error: {e}")
        return None
    except Exception as e:
        print(e)
        return None
    finally:
        if con:
            con.close()

def check_book_availability(book_id):
    try:
        book = get_book_by_id(book_id)
        if isinstance(book, Response):
            book_data = book.get_json()
        else:
            return jsonify({"error": "Could not find the book in the database."})
        return book_data['available']
    except Error as e:
        return jsonify({"error": f"Could not check book availability: {e}"})

def delete_book(book_id):
    try:
        con = connect_db()
        with con:
            check_loan = 'SELECT * FROM emprestimo WHERE id_livro = ? AND data_devolvido IS NULL'
            delete_query = 'DELETE FROM livro WHERE id_livro = ?'
            cursor = con.execute(check_loan, (book_id,))
            is_loaned = cursor.fetchall()

            if not is_loaned:
                con.execute(delete_query, (book_id,))
                return jsonify({"message": "Book successfully deleted!"})    
            else:
                return jsonify({"error": "Cannot delete the book because it is currently on loan."})
    except Error as e:
        return jsonify({"error": f"Failed to delete book. This book likely has loan records, deleting it would cause data inconsistency."})
    finally:
        if con:
            con.close()

def get_pending_loans_by_user_id(user_id):
    loans = []
    try:
        con = connect_db()
        with con:
            query = """
            SELECT 
                usuario.nome_usuario,
                livro.titulo_livro,
                emprestimo.data_devolucao,
                emprestimo.data_devolvido,
                emprestimo.data_emprestimo
            FROM
                emprestimo
            JOIN usuario ON emprestimo.id_usuario = usuario.id_usuario
            JOIN livro ON emprestimo.id_livro = livro.id_livro
            WHERE data_devolvido IS NULL AND usuario.id_usuario = ?
            """
            cursor = con.execute(query, (user_id,))
            rows = cursor.fetchall()
            for row in rows:
                loan = {
                    "user_name": row["nome_usuario"],
                    "book_title": row["titulo_livro"],
                    "due_date": row["data_devolucao"],
                    "returned_date": row["data_devolvido"],
                    "loan_date": row["data_emprestimo"]
                }
                loans.append(loan)
            return loans
    except Error as e:
        return jsonify({"error": f"Error retrieving loans: {e}"})
    finally:
        if con:
            con.close()

def set_return_date(user_id, book_id):
    try:
        con = connect_db()
        today = date.today()
        with con:
            update_query = """UPDATE emprestimo SET data_devolvido = ? WHERE id_usuario = ? AND id_livro = ?"""
            con.execute(update_query, (today.isoformat(), user_id, book_id))
    except Error as e:
        print(f"Error executing return: {e}")
        return
    finally:
        if con:
            con.close()
