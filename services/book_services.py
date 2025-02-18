from models.biblioteca import Usuario, Biblioteca, Livro
import random
import datetime
import db 
usuarios = []
biblioteca = Biblioteca()
import utils
from flask import jsonify, request, Flask, Response
from marshmallow import Schema, fields, validate, ValidationError


def cadastra_livro():
    try:
        
        dados = request.get_json()

        livro_schema = utils.LivroSchema()
        try:

            livro = livro_schema.load(dados)
        except ValidationError as err:
            return jsonify({"erro": "Dados inválidos", "detalhes": err.messages}), 400

        titulo = livro.get('titulo')
        autor = livro.get('autor')
        ano = livro.get('ano')
        
        resposta = db.inserir_livro(titulo, autor, ano, disponivel_livro=1)

        return jsonify({"mensagem": "Livro cadastrado com sucesso!"}), 200
    
    except Exception as e:
        return jsonify({f"Erro":"Erro inesperado: {e}"}), 500
    

def deleta_livro():
    try:
        dados = request.get_json()
        id_livro_schema = utils.IDSchema()

        try:
            id_livro = id_livro_schema.load(dados)
        except ValidationError as err:
            jsonify({"erro":"Dados inválidos", "detalhes":err.messages})
        
        id_livro = id_livro.get("id")

        resposta = db.deletaLivro(id_livro)
        return resposta, 201
    
    except Exception as e:
        return jsonify({f"Erro":"Erro inesperado: {e}"}), 500

def buscar_livro():
    try:
        dados = request.get_json()
        id_livro_schema = utils.IDSchema()

        try:
            id_livro = id_livro_schema.load(dados)
        except ValidationError as err:
            jsonify({"erro":"Dados inválidos", "detalhes":err.messages})
        
        id_livro = id_livro.get("id")
        
        # verifica se o livro existe no BD
        verifica_livro = db.busca_livro_por_id(id_livro)
        
        if verifica_livro is None:
            return jsonify({"erro":"Não foi possível encontrar o livro"}), 404

        # caso sim, retorna o livro
        resposta = db.busca_livro_por_id(id_livro)
        return resposta, 200
    except Exception as e:
        return jsonify({"Erro":f"Erro inesperado: {e}"}), 500
        
def emprestar_livro_para_usuario():
    try:
        # recebe os dados da requisição
        dados = request.get_json()

        # valida o id do usuario
        id_usuario_schema = utils.IDSchema()
        try:
            id_usuario = id_usuario_schema.load({"id":dados.get("id_usuario")})
        except ValidationError as err:
            return jsonify({"erro":"Dados inválidos", "detalhes":err.messages}), 400

        id_usuario = id_usuario.get("id")    


        # recebe ID livro e valida
        id_livro_schema = utils.IDSchema()

        try:
            id_livro = id_livro_schema.load({"id":dados.get("id_livro")})
        except ValidationError as err:
            return jsonify({"erro":"Dados inválidos", "detalhes":err.messages}), 400


        id_livro = id_livro.get("id")


        # verifica se o usuario existe no BD
        verifica_usuario = db.busca_usuario_por_id(id_usuario)
        if verifica_usuario is None:
            return jsonify({"erro":"Não foi possível encontrar o usuário"}), 404
        
        # verifica se o livro existe no BD
        verifica_livro = db.busca_livro_por_id(id_livro)
        if verifica_livro is None:
            return jsonify({"erro":"Não foi possível encontrar o usuário"}), 404
        
        #verificando se o livro está disponível
        esta_disponivel = db.verifica_disponibilidade_livro(id_livro)
        
        if not esta_disponivel:
            return jsonify({"erro":"O livro não está disponível para empréstimo"}), 409
        
        resposta = db.inserir_emprestimo(id_livro, id_usuario)
        return resposta, 201   
        
    except Exception as e:
        return jsonify({"Erro":f"Erro inesperado: {e}"}), 500
    
def devolver_livro_emprestado():
    try:
        # recebe os dados da requisição
        dados = request.get_json()

        #recebe id de usuario e valida 
        id_usuario_schema = utils.IDSchema()

        try:
            id_usuario = id_usuario_schema.load({"id":dados.get("id_usuario")})
        except ValidationError as err:
            return jsonify({"erro":"Dados inválidos", "detalhes":err.messages}), 400
        
        id_usuario = id_usuario.get("id")


        #recebe id_livro e valida
        id_livro_schema = utils.IDSchema()

        try:
            id_livro = id_livro_schema.load({"id":dados.get("id_livro")})
        except ValidationError as err:
            return jsonify({"erro":"Dados inválidos", "detalhes":err.messages}), 400
        
        id_livro = id_livro.get("id")

        # verifica se o usuario existe no BD
        verifica_usuario = db.busca_usuario_por_id(id_usuario)
        if verifica_usuario is None:
            return jsonify({"erro":"Não foi possível encontrar o usuário"}), 404
        
        # verifica se o livro existe no BD
        verifica_livro = db.busca_livro_por_id(id_livro)

        if isinstance(verifica_livro, Response):
            livro_data = verifica_livro.get_json()

        if verifica_livro is None:
            return jsonify({"erro":"Não foi possível encontrar o livro"}), 404

        

        
        
        # verifica se o livro se encontra na lista de livros emprestados pelo usuário e realmente n foi devolvido
        emprestimos_do_usuario = db.consulta_emprestimo_pendente_por_id_usuario(id_usuario)
        emprestimo_encontrado = None
        for emprestimo in emprestimos_do_usuario:
            if livro_data['titulo'].lower() == emprestimo['titulo_livro'].lower():
                emprestimo_encontrado = emprestimo['titulo_livro'].lower()

        if emprestimo_encontrado is None:
            return jsonify({"erro":"Este livro não foi emprestado por esse usuário ou já foi devolvido."}), 409
        # Marca data de devolvido na tabela de devoluções
        db.marca_data_de_devolvido_livro_por_id_usuario_e_id_livro(id_usuario, id_livro)

        # Torna livro disponível
        resposta = db.disponibilizar_livro(id_livro)
        return resposta, 201
    except Exception as e:
        return jsonify({"Erro":f"Erro inesperado: {e}"}), 500

def lista_livros_emprestados_usuario():
    try:
        dados = request.get_json()
        id_schema = utils.IDSchema()
        
        try:
            id_usuario = id_schema.load(dados)
        except ValidationError as err:
            return jsonify({"erro": "Dados inválidos", "detalhes":err.messages})
    

        id_usuario = id_usuario.get("id")

        
        #verifica se usuário existe
        verifica_usuario = db.busca_livro_por_id(id_usuario)
        if verifica_usuario is None:
            return jsonify({"Erro": "Não foi possível encontrar o usuário"}), 404

        #busca os livros na tabela empréstimo
        resposta = db.consulta_emprestimo_pendente_por_id_usuario(id_usuario)

        if not resposta:
            return jsonify([]), 200  # Retorna uma lista vazia se não houver empréstimos
        
        return jsonify(resposta), 200
    
    except Exception as e:
        return jsonify({"erro":f"Erro inesperado: {e}"}), 500