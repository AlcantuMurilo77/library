import models
import services
import services.book_services
import db, utils


from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/listarlivros", methods=['GET']) 
def listar_livros():
        livros = db.consultar_livros()
        return jsonify(livros)

@app.route("/cadastrarlivro", methods=['POST']) 
def cadastra_livro_api():
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
        return resposta

    except Exception as e:
        return jsonify({"erro": f"Erro inesperado {e}"}), 500


@app.route("/listarusuarios", methods=['GET']) 
def lista_usuarios_api():
    usuarios = db.consultar_clientes()
    return jsonify(usuarios)

@app.route("/cadastrarusuario", methods=['POST']) 
def cadastrar_usuario_api():
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

@app.route("/exibirlivrosemprestadosporusuario", methods=['POST'])
def lista_livros_emprestados_usuario():
    try:
        dados = request.get_json()
        if dados is None:
            return jsonify({"Erro":"Corpo da requisição não é um JSON válido"}), 400
        #recebe id usuario e valida
        id_usuario = dados.get("id_usuario")
        valido, mensagem = utils.validar_id(id_usuario)
        if not valido:
            return jsonify({"Erro": mensagem})
        
        #verifica se usuário existe
        verifica_usuario = db.busca_livro_por_id(id_usuario)
        if verifica_usuario is None:
            return jsonify({"Erro": "Não foi possível encontrar o usuário"})

        #busca os livros na tabela empréstimo
        resposta = db.consulta_emprestimo_pendente_por_id_usuario(id_usuario)
        return jsonify(resposta)
    
    except Exception as e:
        return jsonify({"erro":f"Erro inesperado: {e}"})

@app.route("/emprestarlivro", methods=["POST"])
def emprestar_livro_para_usuario():
    try:
        # recebe ID do usuário e valida
        dados = request.get_json()
        id_usuario = dados.get("id_usuario")
        valido, mensagem = utils.validar_id(id_usuario)
        if not valido:
            return jsonify({"Erro": mensagem})

        # recebe ID livro e valida
        id_livro = dados.get("id_livro")
        valido, mensagem = utils.validar_id(id_livro)
        if not valido:
            return jsonify({"Erro": mensagem})

        # verifica se o usuario existe no BD
        verifica_usuario = db.busca_usuario_por_id(id_usuario)
        if verifica_usuario is None:
            return jsonify({"erro":"Não foi possível encontrar o usuário"})
        
        # verifica se o livro existe no BD
        verifica_livro = db.busca_livro_por_id(id_livro)
        if verifica_livro is None:
            return jsonify({"erro":"Não foi possível encontrar o usuário"})
        
        #verificando se o livro está disponível
        esta_disponivel = db.verifica_disponibilidade_livro(id_livro)
        
        if esta_disponivel:
            resposta = db.inserir_emprestimo(id_livro, id_usuario)
            return resposta
        else:
            return jsonify({"erro":"O livro não está disponível para empréstimo"})
    except Exception as e:
        return jsonify({"Erro":f"Erro inesperado: {e}"})
    

@app.route("/devolverlivro", methods=['POST']) 
def devolver_livro_emprestado():
    try:
        dados = request.get_json()

        #recebe id de usuario e valida 
        id_usuario = dados.get("id_usuario")
        valido, mensagem = utils.validar_id(id_usuario)
        if not valido:
            return jsonify({"Erro": mensagem})
        
        #recebe id_livro e valida (VALIDAR)
        id_livro = dados.get("id_livro")
        valido, mensagem = utils.validar_id(id_livro)
        if not valido:
            return jsonify({"Erro": mensagem})

        # verifica se o usuario existe no BD
        verifica_usuario = db.busca_usuario_por_id(id_usuario)
        if verifica_usuario is None:
            return jsonify({"erro":"Não foi possível encontrar o usuário"})
        
        # verifica se o livro existe no BD
        verifica_livro = db.busca_livro_por_id(id_livro)
        if verifica_livro is None:
            return jsonify({"erro":"Não foi possível encontrar o usuário"})
        
        # verifica se o livro se encontra na lista de livros emprestados pelo usuário e realmente n foi devolvido
        emprestimos_do_usuario = db.consulta_emprestimo_pendente_por_id_usuario(id_usuario)
        emprestimo_encontrado = None
        for emprestimo in emprestimos_do_usuario:
            if verifica_livro.titulo.lower() == emprestimo[1]:
                emprestimo_encontrado = emprestimo[1]

        if emprestimo_encontrado is None:
            return jsonify({"erro":"Este livro não foi emprestado por esse usuário ou já foi devolvido."})
        # Marca data de devolvido na tabela de devoluções
        db.marca_data_de_devolvido_livro_por_id_usuario_e_id_livro(id_usuario, id_livro)

        # Torna livro disponível
        resposta = db.disponibilizar_livro(id_livro)
        return resposta
    except Exception as e:
        return jsonify({"Erro":f"Erro inesperado: {e}"})

@app.route("/buscarlivro", methods=['POST']) 
def buscar_livro():
    try:
        dados = request.get_json()
        #Recebe o ID do livro e valida
        id_livro = dados.get("id_livro")
        valido, mensagem = utils.validar_id(id_livro)
        if not valido:
            return jsonify({"Erro": mensagem})

        # verifica se o livro existe no BD
        verifica_livro = db.busca_livro_por_id(id_livro)
        if verifica_livro is None:
            return jsonify({"erro":"Não foi possível encontrar o usuário"})

        # caso sim, retorna o livro
        resposta = db.busca_livro_por_id(id_livro)
        return resposta
    except Exception as e:
        return jsonify({"Erro":f"Erro inesperado: {e}"})
    
@app.route("/deletalivro", methods=["POST"]) 
def deleta_livro():
    try:
        dados = request.get_json()

        #recebe id do livro e valida
        id_livro = dados.get("id_livro")
        valido, mensagem = utils.validar_id(id_livro)
        if not valido:
            return jsonify({"Erro": mensagem})
        resposta = db.deletaLivro(id_livro)
        return resposta
    except Exception as e:
        return jsonify({f"Erro":"Erro inesperado: {e}"})

if __name__ == '__main__':
    app.run()