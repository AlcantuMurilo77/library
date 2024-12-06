import services.book_services as book_services
import services.user_services as user_services
from models.biblioteca import Usuario, Biblioteca, Livro # Importa as classes Usuario, Biblioteca e Livro
import services.book_services as book_services # Importa o módulo com funções auxiliares
from services.book_services import usuarios, biblioteca # importa dados e objetos globais
getout = True # Controla a execução do loop principal do menu
import db

while getout == True:
    print("MENU")
    print("1.Opções de Usuários\n2.Opções de Biblioteca\n3.Sair\n")

    try:
        opt1 = int(input(">> ")) # Recebe a opção do usuário
    except ValueError:
        print("Erro: Por favor, insira um número válido (1, 2 ou 3)")
        continue # Reinicia o loop para que o dado seja inserido corretamente

    if opt1 == 1:

        print("1.Cadastrar Usuário\n2.Exibir Usuários\n3.Exibir Livros emprestados\n4.Emprestar Livro\n5.Devolver Livro\n")

        try:
            opt = int(input(">> ")) # Recebe a opção do usuário e tenta converter para inteiro
        except ValueError:
            print("Erro: Por favor, insira um número válido (1-5)")
            continue # Reinicia o loop para que o dado seja inserido corretamente

        if opt == 1:
            user_services.cadastraUsuario() # Cadastra um novo usuario na lista "usuários"

        elif opt == 2:
            print("Usuários Cadastrados: ")
            db.consultar_clientes()
            
        elif opt == 3:
            book_services.livros_emprestados_por_usuario() # Exibe livros emprestados por um usuário


        elif opt == 4:
            book_services.emprestaLivro() # Chama a função para emprestar livro para um usuário


        elif opt == 5:
            book_services.devolveLivro() # Chama a função para devolver livro para um usuário
        
    elif opt1 == 2:
        print("1.Adicionar Livro\n2.Deletar Livro\n3.Buscar Livro\n4.Listar Livros\n")

        try:
            opt2 = int(input(">> ")) # Recebe a opção do usuário
        except ValueError:
            print("Erro: Por favor, insira um número válido (1-5)")
            continue # Reinicia o loop para que o dado seja inserido corretamente

        if opt2 == 1:
            book_services.cadastraLivro() # Chama a função para cadastro de um novo livro
        
        elif opt2 == 2:
            book_services.deletaLivro() # Chama a função que deleta um livro 

        elif opt2 == 3:
            book_services.buscaLivro() # Chama a função que busca por um livro específico

        elif opt2 == 4:
            print("LIVROS:")
            db.consultar_livros()
    
    elif opt1 == 3:
        getout = False # Encerra o programa ao sair do loop