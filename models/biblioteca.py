import db
from db import con
from mysql.connector import Error

class Livro:
    titulo:str
    autor:str
    ano:int
    id:int
    def __init__(self, titulo, autor, ano, id, disponivel):
        self.titulo = titulo
        self.autor = autor
        self.ano = ano
        self.id = id
        self.disponivel = disponivel
    
    def emprestar(self):
        self.disponivel = False

    def devolver(self):
        self.disponivel = True
    
    def showdisponivel(self):
        return "Disponível" if self.disponivel else "Não disponível"
    
    def __repr__(self):
        return f"<Livro {self.titulo}, Autor {self.autor}, Lançado em {self.ano}, Disponibilidade: {self.showdisponivel()}>"

class Usuario:
    nome:str
    def __init__(self, nome, id):
        self.nome = nome
        self.livros_emprestados = []
        self.id = id

    def emprestarLivro(self, livro):
        if livro.disponivel:
            self.livros_emprestados.append(livro)
            livro.emprestar()
    
    def devolverLivro(self, livro):
        if livro in self.livros_emprestados:
            self.livros_emprestados.remove(livro)
            livro.devolver()

class Biblioteca:
    def __init__(self):
        self.catalogo = []
    
    def adicionarLivro(self, livro):
        self.catalogo.append(livro)

    def buscarLivro(self, titulo):
        encontrou = False
        for livro in self.catalogo:
            if livro.titulo.upper() == titulo.upper():
                print(f"Livro encontrado: Título: {livro.titulo}|Autor: {livro.autor}| Ano de lançamento: {livro.ano}| Disponibilidade; {livro.showdisponivel()}| ID: {livro.id}")
                encontrou = True
                break

    def listarDisponiveis(self):
        print("Livros disponíveis: \n")
        for livro in self.catalogo:
            if livro.disponivel:
                print(f"- {livro}\n")
            else:
                pass

