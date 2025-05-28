import mysql.connector
from mysql.connector import Error
import models.library as library
from datetime import timedelta, date
from flask import jsonify, Response

con = None

def connect_db():
    global con
    try:
        con = mysql.connector.connect(
            host='localhost',
            database='biblioteca',
            user='murilo',
            password='*'
        )
    except Error as e:
        print(f"Failed to connect to the database: {e}")

def insert_user(nome_usuario):
    global con
    try:
        connect_db()
        insert_query = """INSERT INTO usuario (nome_usuario) VALUES (%s)"""
        cursor = con.cursor()
        cursor.execute(insert_query, (nome_usuario,))
        con.commit()
    except Error as e:
        raise Exception(f"Failed to insert user: {e}")
    finally:
        if con.is_connected():
            cursor.close()
            con.close()

def insert_book(title, author, year, available):
    global con
    try:
        available = 1
        connect_db()
        insert_query = """INSERT INTO livro (titulo_livro, autor_livro, ano_livro, disponivel_livro) VALUES (%s, %s, %s, %s)"""
        cursor = con.cursor()
        cursor.execute(insert_query, (title, author, year, available))
        con.commit()
        return {"message": "Book successfully added!"}
    except Error as e:
        return {"error": f"Failed to insert book: {e}"}
    finally:
        if con.is_connected():
            cursor.close()
            con.close()

def make_book_available(book_id):
    try:
        global con
        connect_db()
        query = """UPDATE livro SET disponivel_livro = 1 WHERE livro.id_livro = %s"""
        cursor = con.cursor()
        cursor.execute(query, (book_id,))
        con.commit()
        return jsonify({"message": "Book successfully returned!"})
    except Error as e:
        print(f"Error making book available: {e}")
        return
    finally:
        if con.is_connected():
            cursor.close()
            con.close()

def insert_loan(book_id, user_id):
    global con
    try:
        today = date.today()
        due_date = today + timedelta(days=15)
        connect_db()
        insert_query = """INSERT INTO emprestimo (id_usuario, id_livro, data_emprestimo, data_devolucao) VALUES (%s, %s, %s, %s)"""
        cursor = con.cursor()
        cursor.execute(insert_query, (user_id, book_id, today, due_date))
        con.commit()

        update_query = """UPDATE livro SET disponivel_livro = 0 WHERE livro.id_livro = %s"""
        cursor.execute(update_query, (book_id,))
        con.commit()
        
        return jsonify({"message": "Loan successfully registered!"})
    except Error as e:
        print("Failed to insert data into the DB: ", e)
        return
    finally:
        if con.is_connected():
            cursor.close()
            con.close()

def get_users():
    global con
    users = []
    try:
        connect_db()
        query = 'SELECT * FROM usuario'
        cursor = con.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            users.append({"id": row[0], "name": row[1]})
        return users
    except Error as e:
        print(f"Failed to query the table: {e}")
        return Exception("Database error: " + e.msg)
    finally:
        if con.is_connected():
            cursor.close()
            con.close()

def get_user_by_id(user_id: int):
    global con
    try:
        connect_db()
        query = 'SELECT * FROM usuario WHERE id_usuario = %s'
        cursor = con.cursor()
        cursor.execute(query, (user_id,))
        rows = cursor.fetchall()
        return library.Usuario(nome=rows[0][1], id=rows[0][0])
    except Error as e:
        return jsonify({"error": f"Error fetching user: {e}"})
    finally:
        if con.is_connected():
            cursor.close()
            con.close()

def get_books():
    global con
    books = []
    try:
        connect_db()
        query = 'SELECT * FROM livro'
        cursor = con.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            book = {
                "id": row[0],
                "title": row[1],
                "author": row[2],
                "year": row[3],
                "available": "Available" if row[4] else "Unavailable"
            }
            books.append(book)
        return books
    except Error as e:
        print(f"Failed to query the table: {e}")
        return
    finally:
        if con.is_connected():
            cursor.close()
            con.close()

def get_book_by_id(book_id):
    global con
    try:
        connect_db()
        query = 'SELECT * FROM livro WHERE id_livro = %s'
        cursor = con.cursor()
        cursor.execute(query, (book_id,))
        rows = cursor.fetchall()
        if not rows:
            return None
        book = library.Livro(rows[0][1], rows[0][2], rows[0][3], rows[0][0], disponivel=rows[0][4])
        return jsonify({
            "id": book.id,
            "title": book.titulo,
            "author": book.autor,
            "year": book.ano,
            "available": book.disponivel
        })
    except mysql.connector.Error as db_err:
        print(f"Database error: {db_err}")
        return None
    except Exception as e:
        print(e)
        return None
    finally:
        if con.is_connected():
            cursor.close()
            con.close()

def check_book_availability(book_id):
    global con
    try:
        book = get_book_by_id(book_id)
        if isinstance(book, Response):
            book_data = book.get_json()
        book_data = book.get_json()
        if not book_data:
            return jsonify({"error": "Could not find the book in the database."})
        return book_data['available']
    except Error as e:
        return jsonify({"error": f"Could not check book availability: {e}"})

def delete_book(book_id):
    global con
    try:
        connect_db()
        check_loan = 'SELECT * FROM emprestimo WHERE id_livro = %s AND data_devolvido IS NULL'
        delete_query = 'DELETE FROM livro WHERE id_livro = %s'
        cursor = con.cursor()
        cursor.execute(check_loan, (book_id,))
        is_loaned = cursor.fetchall()

        if not is_loaned:
            cursor.nextset()
            cursor.execute(delete_query, (book_id,))
            con.commit()
            return jsonify({"message": "Book successfully deleted!"})    
        else:
            return jsonify({"error": "Cannot delete the book because it is currently on loan."})
    except Error as e:
        return jsonify({"error": f"Failed to delete book. This book likely has loan records, deleting it would cause data inconsistency."})
    finally:
        if con.is_connected:
            cursor.close()
            con.close()

def get_pending_loans_by_user_id(user_id):
    try:
        global con
        loans = []
        connect_db()
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
        WHERE data_devolvido IS NULL AND usuario.id_usuario = %s
        """
        cursor = con.cursor()
        cursor.execute(query, (user_id,))
        rows = cursor.fetchall()
        for row in rows:
            loan = {
                "user_name": row[0],
                "book_title": row[1],
                "due_date": row[2],
                "returned_date": row[3],
                "loan_date": row[4]
            }
            loans.append(loan)
            return loans
    except Error as e:
        return jsonify({"error": f"Error retrieving loans: {e}"})
    finally:
        if con.is_connected():
            cursor.close()
            con.close()

def set_return_date(user_id, book_id):
    try:
        global con
        connect_db()
        today = date.today()
        update_query = """UPDATE emprestimo SET data_devolvido = %s WHERE id_usuario = %s AND id_livro = %s"""
        cursor = con.cursor()
        cursor.execute(update_query, (today, user_id, book_id))
        con.commit()
    except Error as e:
        print(f"Error executing return: {e}")
        return
    finally:
        if con.is_connected():
            cursor.close()
            con.close()
