from models.biblioteca import Usuario, Biblioteca, Livro
import random
import datetime
import db 
usuarios = []
biblioteca = Biblioteca()
import utils
from flask import jsonify, request, Flask

def cadastra_livro():
    try:
        
        dados = request.get_json()
        if dados is None:
            return jsonify({"erro": "corpo da requisição não é um JSON válido"}), 400

        titulo = dados.get('titulo')
        autor = dados.get('autor')
        ano = dados.get('ano')
        
        if not titulo or not autor or not ano:
            return jsonify({"erro": "Campos 'titulo', 'autor' e 'ano' são obrigatórios."}), 400
        
        # Aqui, adicionei a validação de tipo para o ano, caso seja necessário garantir que é um número.
        try:
            ano = int(ano)  # Garantindo que ano seja convertido para inteiro
        except ValueError:
            return jsonify({"erro": "Ano deve ser um número válido."}), 400
        
        resposta = db.inserir_livro(titulo, autor, ano)
        return resposta, 201

    except Exception as e:
        return jsonify({"erro": f"Erro inesperado {e}"}), 500
    

def deleta_livro():
    try:
        dados = request.get_json()

        #recebe id do livro e valida
        id_livro = dados.get("id_livro")
        valido, mensagem = utils.validar_id(id_livro)
        if not valido:
            return jsonify({"Erro": mensagem}), 400
        resposta = db.deletaLivro(id_livro)
        return resposta, 201
    except Exception as e:
        return jsonify({f"Erro":"Erro inesperado: {e}"}), 500

def buscar_livro():
    try:
        dados = request.get_json()
        #Recebe o ID do livro e valida
        id_livro = dados.get("id_livro")
        valido, mensagem = utils.validar_id(id_livro)
        if not valido:
            return jsonify({"Erro": mensagem}), 400

        # verifica se o livro existe no BD
        verifica_livro = db.busca_livro_por_id(id_livro)
        if verifica_livro is None:
            return jsonify({"erro":"Não foi possível encontrar o usuário"}), 404

        # caso sim, retorna o livro
        resposta = db.busca_livro_por_id(id_livro)
        return resposta, 200
    except Exception as e:
        return jsonify({"Erro":f"Erro inesperado: {e}"}), 500
        
def emprestar_livro_para_usuario():
    try:
        # recebe ID do usuário e valida
        dados = request.get_json()
        id_usuario = dados.get("id_usuario")
        valido, mensagem = utils.validar_id(id_usuario)
        if not valido:
            return jsonify({"Erro": mensagem}), 400

        # recebe ID livro e valida
        id_livro = dados.get("id_livro")
        valido, mensagem = utils.validar_id(id_livro)
        if not valido:
            return jsonify({"Erro": mensagem}), 400

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
        
        if esta_disponivel:
            resposta = db.inserir_emprestimo(id_livro, id_usuario)
            return resposta, 201
        else:
            return jsonify({"erro":"O livro não está disponível para empréstimo"}), 409
    except Exception as e:
        return jsonify({"Erro":f"Erro inesperado: {e}"}), 500
    
def devolver_livro_emprestado():
    try:
        dados = request.get_json()

        #recebe id de usuario e valida 
        id_usuario = dados.get("id_usuario")
        valido, mensagem = utils.validar_id(id_usuario)
        if not valido:
            return jsonify({"Erro": mensagem}), 400
        
        #recebe id_livro e valida (VALIDAR)
        id_livro = dados.get("id_livro")
        valido, mensagem = utils.validar_id(id_livro)
        if not valido:
            return jsonify({"Erro": mensagem}), 400

        # verifica se o usuario existe no BD
        verifica_usuario = db.busca_usuario_por_id(id_usuario)
        if verifica_usuario is None:
            return jsonify({"erro":"Não foi possível encontrar o usuário"}), 404
        
        # verifica se o livro existe no BD
        verifica_livro = db.busca_livro_por_id(id_livro)
        if verifica_livro is None:
            return jsonify({"erro":"Não foi possível encontrar o livro"}), 404
        
        # verifica se o livro se encontra na lista de livros emprestados pelo usuário e realmente n foi devolvido
        emprestimos_do_usuario = db.consulta_emprestimo_pendente_por_id_usuario(id_usuario)
        emprestimo_encontrado = None
        for emprestimo in emprestimos_do_usuario:
            if verifica_livro.titulo.lower() == emprestimo[1]:
                emprestimo_encontrado = emprestimo[1]

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
        if dados is None:
            return jsonify({"Erro":"Corpo da requisição não é um JSON válido"}), 400
        #recebe id usuario e valida
        id_usuario = dados.get("id_usuario")
        valido, mensagem = utils.validar_id(id_usuario)
        if not valido:
            return jsonify({"Erro": mensagem}), 400
        
        #verifica se usuário existe
        verifica_usuario = db.busca_livro_por_id(id_usuario)
        if verifica_usuario is None:
            return jsonify({"Erro": "Não foi possível encontrar o usuário"}), 404

        #busca os livros na tabela empréstimo
        resposta = db.consulta_emprestimo_pendente_por_id_usuario(id_usuario)
        return jsonify(resposta), 200
    
    except Exception as e:
        return jsonify({"erro":f"Erro inesperado: {e}"}), 500