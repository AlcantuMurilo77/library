from models.biblioteca import Usuario, Biblioteca, Livro
import random
import datetime
import db 
usuarios = []
biblioteca = Biblioteca()
import utils
from flask import jsonify

def cadastraLivro(titulo, autor, ano):

    if not titulo or not autor:
        return jsonify({"Erro": "Titulo e/ou autor não podem estar vazio."}), 400
        
    #Adiciona o livro à biblioteca
    db.inserir_livro(titulo, autor, ano, True)
    return jsonify({"Mensagem": f"Livro '{titulo}' adicionado com sucesso!"})
    

def deletaLivro():
    # Recebe ID do livro e valida
    livro_deletar = utils.obter_numero("Digite o ID do livro: ")

    # verificando se o livro existe no banco de dados e deletando
    db.deletaLivro(livro_deletar)

def buscaLivro():
    try:
        # Recebe ID do livro e valida
        livro_emprestado = utils.obter_numero("Digite o ID do livro: ")

        # verificando se o livro existe no banco de dados e retornando uma instancia de Livro
        livro_encontrado = db.busca_livro_por_id(livro_emprestado)
        if livro_encontrado is None:
            print(f"Erro: Não foi possível encontrar o livro.")
            return
        
        print(f"ID: {livro_encontrado.id} | Título: {livro_encontrado.titulo} | Autor: {livro_encontrado.autor} | Ano de Lançamento: {livro_encontrado.ano} | Disponibilidade: {'Disponível' if livro_encontrado.disponivel else 'Indisponível'}")
    
    except Exception as e:
        print(f"Erro inesperado ao buscar livro: {e}")
        
def emprestaLivro():
    # Recebe o ID do usuário e valida
    usuario_empresta = utils.obter_numero("Digite o ID do usuário: ")

    # verificando se o usuario existe no banco de dados e retornando uma instancia de Usuario
    usuario_encontrado = db.busca_usuario_por_id(usuario_empresta) ## retorna a instancia de usuario
    if usuario_encontrado == None:
        print(f"Erro: Não foi possível encontrar o usuário '{usuario_empresta}'.")
        return
    input(f"Nome do usuario encontrado:{usuario_encontrado.nome}" )

    # Recebe ID do livro e valida
    livro_emprestado = utils.obter_numero("Digite o ID do livro: ")

    # verificando se o livro existe no banco de dados e retornando uma instancia de Livro
    livro_encontrado = db.busca_livro_por_id(livro_emprestado)

    if livro_encontrado == None:
        print(f"Erro: Não foi possível encontrar o livro.")
        return

    # Verificando se o livro está disponível
    disponivel = db.verifica_disponibilidade_livro(livro_emprestado)
    if disponivel:
        db.inserir_emprestimo(livro_emprestado, usuario_empresta)
        print(f"Livro '{livro_encontrado.titulo}' emprestado com sucesso!")

    else:
        print(f"Erro: O livro '{livro_encontrado.titulo}' não está disponível para ser emprestado!.")
    
def devolveLivro():
    # Recebe id de usuário e valida
    usuario_devolve = utils.obter_numero("Qual o ID do usuário que fará a devolução?: ")

    # Verifica se o usuário existe e retorna instancia
    usuario_encontrado = db.busca_usuario_por_id(usuario_devolve)
    if usuario_encontrado == None:
        print(f"Erro: Não foi possível encontrar o usuário.")
        return
   
     # Recebe ID do livro e valida
    livro_emprestado = utils.obter_numero("Digite o ID do livro: ")

    # verificando se o livro existe no banco de dados e retornando uma instancia de Livro
    livro_encontrado = db.busca_livro_por_id(livro_emprestado)
    if livro_encontrado == None:
        print(f"Erro: Não foi possível encontrar o livro '{livro_emprestado}'.")
        return

    # verifica se o livro se encontra na lista de livros emprestados pelo usuário em questão, e se realmente n foi devolvido ainda
    emprestimos = db.consulta_emprestimo_pendente_por_id_usuario(usuario_encontrado.id)
    emprestimo_encontrado = None
    for emprestimo in emprestimos:
        if livro_encontrado.titulo.lower() == emprestimo[1]:
            emprestimo_encontrado = emprestimo[1]
    
    if emprestimo_encontrado == None:
        print(f"Erro: Este livro não foi emprestado por esse usuário ou já foi devolvido")

    # Marca data de devolvido na tabela de devoluções
    db.marca_data_de_devolvido_livro_por_id_usuario_e_id_livro(usuario_encontrado.id, livro_encontrado.id)

    #torna livro disponível
    db.disponibilizar_livro(livro_encontrado.id)

def livros_emprestados_por_usuario():
     # Recebe id de usuário e valida
    usuario_devolve = utils.obter_numero("Qual o ID do usuário do qual deseja ver os empréstimos?: ")

    # Verifica se o usuário existe
    usuario_encontrado = db.busca_usuario_por_id(usuario_devolve)
    if usuario_encontrado == None:
        print(f"Erro: Não foi possível encontrar o usuário '{usuario_devolve}'.")
        return

    #Busca os livros na tabela empréstimo
    emprestimos_feitos_por_usr = (db.consulta_emprestimo_pendente_por_id_usuario(usuario_encontrado.id))
    for emprestimo in emprestimos_feitos_por_usr:
        print(f"Livro: {emprestimo[1]} | Data de emprestimo: {emprestimo[4]} | Data de devolução: {emprestimo[2]}")
