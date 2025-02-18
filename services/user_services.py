from models.biblioteca import Usuario, Biblioteca, Livro
import random
import datetime
import db 
biblioteca = Biblioteca()
import utils
from flask import Flask, request, jsonify
from marshmallow import Schema, fields, validate, ValidationError

def cadastrar_usuario():
    try:

        dados = request.get_json()

        usuario_schema = utils.UsuarioSchema()
        try:
            usuario = usuario_schema.load(dados)
        except ValidationError as err:
            return jsonify({"erro": "Dados inválidos", "detalhes":err.messages}), 400
        

        nome_usuario = usuario.get('nome_usuario')
         
        resposta = db.inserir_cliente(nome_usuario)

        return jsonify({"mensagem":"Usuario cadastrado com sucesso"}), 200
    
    except Exception as e:
        return jsonify({"erro":f"Erro inesperado: {e}"}), 500
    
