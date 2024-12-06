import re

def solicitar_input_com_confirmacao(pergunta, tipo="string", validacao=None, mensagem_erro="Entrada Inválida."):
    while True:
        entrada = input(pergunta).strip()

        # Verificando o tipo de dado
        if tipo == "string" and not entrada:
            print(mensagem_erro)
            continue
        
        elif tipo == "int" and not entrada.isdigit():
            print(mensagem_erro)
            continue
        
        # Se for fornecido uma validação, executa a validação
        if validacao and not validacao(entrada):
            continue
        
        # Confirmação do usuário
        confirmar = input(f"Você inseriu '{entrada}'. Deseja continuar? (s/n): ").lower()
        if confirmar == 's':
            return entrada
        else:
            print("Por favor, insira os dados novamente.")

def validar_nome_usuario(nome):
    if not nome:
        print("Erro: O nome não pode estar vazio.")
        return False
    
    if not re.match(r"^[A-Za-zÀ-ÿ\s]+$", nome): #Permitindo apenas letras e espaços
        print("Erro: O nome deve conter apenas letras e espaços.")
        return False
    if not any(c.isupper() for c in nome): #certifica-se que o nome contenha peloi menos uma letra maiuscula
        print("Erro: o nome deve conter pelo menos uma letra maíscula.")
        return False
    return True

def obter_numero(pergunta):
    while True:
        try:
            numero = int(input(pergunta))
            return numero
        except ValueError:
            print("Erro: Por favor, insira um número válido.")

def validar_nome(nome):
    if not nome:
        return False, "O nome não pode estar vazio"

    if not re.match(r"^[A-Za-zÀ-ÿ\s]+$", nome):
        return False, "O nome deve conter apenas letras e espaços."
    
    if not any(c.isupper() for c in nome):
        return False, "O nome deve conter pelo menos uma letra maíscula"
    
    return True, ""

def validar_id(id):

    if id is None:
        return False, "O ID é obrigatório."
    if not isinstance(id, int):
        return False, "O ID deve ser um número inteiro."
    if id <= 0:
        return False, "O ID deve ser um número positivo."
    return True, None


