from models.biblioteca import Usuario, Biblioteca, Livro
import random
import datetime
import db 
biblioteca = Biblioteca()
import utils

def cadastraUsuario():  
    # Recebe o nome do usuário e valida
    nome = utils.solicitar_input_com_confirmacao(
        "Qual o nome completo do novo usuário?: ",
        tipo="string",
        validacao=utils.validar_nome_usuario
    )
    
    if not nome:
        print("Erro: O nome não pode estar vazio.")
        return  # Finaliza a função em caso de erro

    # Cadastra usuário
    db.inserir_cliente(nome_usuario=nome)
    print(f"Usuário {nome} cadastrado com sucesso!")
    
