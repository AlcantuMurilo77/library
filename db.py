import mysql.connector
from mysql.connector import Error
import models.biblioteca as biblioteca
from datetime import timedelta, date
from flask import jsonify, Response

con = None
#Função para conectar ao banco de dados.
def conectar_bd():
    global con
    try:
        
        con = mysql.connector.connect(host='localhost',
                                        database='biblioteca',
                                        user='murilo',
                                        password='BushDid9/11')
    except Error as e:
        print(f"Falha ao conectar ao banco de dados: {e}")

#Função para inserir cliente novo na tabela usuario
def inserir_cliente(nome_usuario):
    global con
    try:
        conectar_bd()
        inserir_usuario = """INSERT INTO usuario
    (nome_usuario)
    VALUES
    (%s)"""
        cursor = con.cursor()
        cursor.execute(inserir_usuario, (nome_usuario,))
        con.commit()

    except Error as e:
        raise Exception(f"Falha ao inserir usuário: {e}")
        
    finally:
        if con.is_connected():
            cursor.close()
            con.close()
            

#Função para inserir livro novo na tabela livro
def inserir_livro(titulo_livro, autor_livro, ano_livro, disponivel_livro):
    global con
    try:
        disponivel_livro = 1
        conectar_bd()
        inserir_livro = """INSERT INTO livro
        (titulo_livro, 
        autor_livro, 
        ano_livro, 
        disponivel_livro)
        VAlUES
        (%s,
        %s,
        %s,
        %s)
        """
        cursor = con.cursor()
        cursor.execute(inserir_livro, (titulo_livro, autor_livro, ano_livro, disponivel_livro))
        con.commit()
        return {"Mensagem":"Livro cadastrado com sucesso!"}
    except Error as e:
        return {"Erro":f"Falha ao inserir livro: {e}"}
    finally:
        if con.is_connected():
            cursor.close()
            con.close()

#Função para deixar livro disponivel
def disponibilizar_livro(idLivro):
    try:
        global con
        conectar_bd()
        deixarLivro_disponivel = """UPDATE livro set disponivel_livro = 1
            WHERE livro.id_livro = %s """
        cursor = con.cursor()
        cursor.execute(deixarLivro_disponivel, (idLivro,))
        con.commit()
        return jsonify({"Mensagem":"Livro Devolvido com sucesso!"})
    except Error as e:
        print(f"Erro ao disponibilizar livro: {e}")
        return
    finally:
        if con.is_connected():
            cursor.close()
            con.close()



#Função para inserir emprestimo novo na tabela emprestimo
def inserir_emprestimo(idLivro, idUsuario):
    global con
    try:
        data_atual = date.today()
        data_devolucao = data_atual + timedelta(days=15)
        conectar_bd()
        inserir_emprestimo = """
        INSERT INTO emprestimo (id_usuario, id_livro, data_emprestimo, data_devolucao) 
        VALUES (%s, %s, %s, %s);
        """
        cursor = con.cursor()
        cursor.execute(inserir_emprestimo, (idUsuario, idLivro, data_atual, data_devolucao))
        con.commit()

        deixarLivro_indisponivel = """UPDATE livro set disponivel_livro = 0
        WHERE livro.id_livro = %s """
        cursor.execute(deixarLivro_indisponivel, (idLivro,))
        con.commit()
        
        return jsonify({"Mensagem": "Empréstimo registrado com sucesso!"})
        
    except Error as e:
        print("Falha ao inserir dados no BD: ", e)
        return
    finally:
        if con.is_connected():
            cursor.close()
            con.close()

#Função para consultar usuarios cadastrados
def consultar_clientes():
    global con
    clientes = []
    try:
        conectar_bd()
        consulta_cliente = f'select * from usuario'
        cursor = con.cursor()
        cursor.execute(consulta_cliente)
        colunas = cursor.fetchall()
        for coluna in colunas:
            cliente =  {"id": coluna[0], "nome" :coluna[1]}
            clientes.append(cliente)
        return clientes
    
    except Error as e:
        print(f"Falha ao consultar a tabela: {e}")
        return Exception("Erro no banco de dados: " + e.msg)
    
    finally:
        if con.is_connected():
            cursor.close()
            con.close()

#Funçâo para verificar existencia de usuario espcifico e retornar uma instancia do mesmo em forma de objeto
def busca_usuario_por_id(id_usuario: int):
    global con
    try:
        conectar_bd()
        consulta_clientes = 'select * from usuario where id_usuario = %s'
        cursor = con.cursor()
        cursor.execute(consulta_clientes, (id_usuario,))
        colunas = cursor.fetchall()
        return biblioteca.Usuario(nome=colunas[0][1], id=colunas[0][0])
    except Error as e:
        return jsonify({"erro":f"Erro ao buscar usuário: {e}"})
    finally:
        if con.is_connected():
            cursor.close()
            con.close()


def consultar_livros():
    global con
    livros = []
    try:
        conectar_bd()
        consulta_livro = 'select * from livro'
        cursor = con.cursor()
        cursor.execute(consulta_livro)
        colunas = cursor.fetchall()
        for coluna in colunas:
            livro = {
                "id": coluna[0],
                "titulo": coluna[1],
                "autor": coluna[2],
                "ano": coluna[3],
                "disponivel": "Disponível" if coluna[4] else "Indisponível"
            }
            livros.append(livro)

        return livros
    
    except Error as e:
        print(f"Falha ao consultar a tabela: {e}")
        return
    finally:
        if con.is_connected():
            cursor.close()
            con.close()


#Funçâo para verificar existencia de livro espcifico e retornar uma instancia do mesmo em forma de objeto
def busca_livro_por_id(id_livro):
    global con
    try:
        conectar_bd()
        consulta_livros = 'select * from livro where id_livro = "%s" '
        cursor = con.cursor()
        cursor.execute(consulta_livros, (id_livro,))
        colunas = cursor.fetchall()

        if not colunas:
            return None
        
        livro =  biblioteca.Livro(colunas[0][1], colunas[0][2], colunas[0][3], colunas[0][0], disponivel=colunas[0][4])
        return jsonify({"id":livro.id,
                        "titulo":livro.titulo,
                        "autor":livro.autor,
                        "ano":livro.ano,
                        "disponibilidade":livro.disponivel
        })
    except mysql.connector.Error as db_err:
        print(f"Erro no banco de dados: {db_err}")
        return None
    except Exception as e:
        print(e)
        return None
    finally:
        if con.is_connected():
            cursor.close()
            con.close()
    
#Função para verificar se um livro já não está emprestado
def verifica_disponibilidade_livro(id_livro):
    global con
    try:
        livro = busca_livro_por_id(id_livro)
        if isinstance(livro, Response):
            livro_data = livro.get_json()

        livro_data = livro.get_json()

        if not livro_data:
            return jsonify({"erro":"Não foi possível encontrar o livro no banco de dados. "})
            
        return livro_data['disponibilidade']
        
    except Error as e:
        return jsonify({"erro":f"Não foi possível verificar a disponibilidade do livro: {e}"})

#Função para deletar livros
def deletaLivro(id_livro):
    global con
    try:
        conectar_bd()
        verificar_emprestimo = 'select * from emprestimo where id_livro = "%s" and data_devolvido=null'
        deletar_livro = 'delete FROM livro WHERE livro.id_livro = "%s"'
        cursor = con.cursor()
        cursor.execute(verificar_emprestimo, (id_livro,))
        estaEmprestado = cursor.fetchall()

        if not estaEmprestado:
            cursor.nextset()
            cursor.execute(deletar_livro, (id_livro,))
            con.commit()
            return jsonify({"mensagem":"Livro deletado com sucesso!"})    
        else:
            return jsonify({"erro":"Não é possível deletar o livro, pois se encontra emprestado."})
            
    except Error as e:
        return jsonify({"erro":f"Falha ao deletar livro. Este livro provavelmente possui um registro de empréstimo, exclui-lo causaria inconsistência de dados."})
        
    finally:
        if con.is_connected:
            cursor.close()
            con.close()     

#Função para consultar empréstimos pendentes de usuario especifico
def consulta_emprestimo_pendente_por_id_usuario(id_usuario):
    try:
        global con
        emprestimos = []
        conectar_bd()
        pesquisa_emprestimo = """SELECT 
        usuario.nome_usuario,
        livro.titulo_livro,
        emprestimo.data_devolucao,
        emprestimo.data_devolvido,
        emprestimo.data_emprestimo
        FROM
            emprestimo
        JOIN
            usuario on emprestimo.id_usuario = usuario.id_usuario
        JOIN
            livro on emprestimo.id_livro = livro.id_livro
        WHERE data_devolvido IS NULL and usuario.id_usuario = "%s" """
        cursor = con.cursor()
        cursor.execute(pesquisa_emprestimo, (id_usuario,))
        colunas = cursor.fetchall()
        for coluna in colunas:
            emprestimo = {
                "nome_usr":coluna[0],
                "titulo_livro":coluna[1],
                "data_devolucao":coluna[2],
                "data_devolvido":coluna[3],
                "data_emprestimo":coluna[4]
            }
            emprestimos.append(emprestimo)
            return emprestimos
        
    except Error as e:
        return jsonify({"erro":f"Erro ao consultar empréstimos: {e}"})
    finally:
        if con.is_connected():
            cursor.close()
            con.close()

def marca_data_de_devolvido_livro_por_id_usuario_e_id_livro(id_usuario, id_livro):
    try:
        global con
        conectar_bd()
        data_atual = date.today()
        marca_devolucao = """UPDATE emprestimo
        SET data_devolvido = %s
        WHERE id_usuario = %s and id_livro = %s;"""
        cursor = con.cursor()
        cursor.execute(marca_devolucao, (data_atual, id_usuario, id_livro))
        con.commit()
    except Error as e:
        print(f"Erro ao executar devolução: {e}")
        return

    finally:
        if con.is_connected():
            cursor.close()
            con.close()