import sqlite3

DB_PATH = 'biblioteca.db'

def create_tables():
    con = sqlite3.connect(DB_PATH)
    cursor = con.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuario (
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_usuario TEXT NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS livro (
        id_livro INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo_livro TEXT NOT NULL,
        autor_livro TEXT NOT NULL,
        ano_livro INTEGER,
        disponivel_livro INTEGER DEFAULT 1 -- 1 = disponível, 0 = indisponível
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS emprestimo (
        id_emprestimo INTEGER PRIMARY KEY AUTOINCREMENT,
        id_usuario INTEGER NOT NULL,
        id_livro INTEGER NOT NULL,
        data_emprestimo TEXT NOT NULL,
        data_devolucao TEXT NOT NULL,
        data_devolvido TEXT, -- data que o livro foi devolvido (pode ser NULL)
        FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
        FOREIGN KEY (id_livro) REFERENCES livro(id_livro)
    )
    """)

    con.commit()
    con.close()

if __name__ == "__main__":
    create_tables()
    print("Banco e tabelas criados com sucesso.")
