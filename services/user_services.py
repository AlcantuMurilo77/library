from models.biblioteca import Usuario, Biblioteca, Livro
import random
import datetime
import db 
biblioteca = Biblioteca()
import utils
from flask import Flask, request, jsonify

def cadastrar_usuario():
    try:

        dados = request.get_json()

        if dados is None:
            return jsonify({"Erro":"Corpo da requisição não é um JSON válido"}), 400
        
        nome_usuario = dados.get("nome_usuario")
       
        #valida nome do usuário
        valido, mensagem = utils.validar_nome(nome_usuario)
        if not valido:
            return jsonify({"erro":mensagem})
         
        resposta = db.inserir_cliente(nome_usuario)
        return resposta
    except Exception as e:
        return jsonify({"erro":f"Erro inesperado: {e}"})
    
