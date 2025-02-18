import re
from marshmallow import Schema, fields, validate, ValidationError
from datetime import datetime

"""
Uso do Marshmallow:

O Marshmallow é utilizado neste projeto para validar e deserializar dados recebidos em requisições HTTP. 
Ele converte dados no formato JSON para objetos Python, aplicando regras de validação para garantir que 
os dados estejam corretos antes de serem processados.

1. Schemas e Validação
   - O Marshmallow utiliza schemas para definir a estrutura dos dados e as validações. No nosso código, temos três schemas:
     - LivroSchema: Valida os dados de um livro (título, autor e ano). O título e o autor devem ser 
     strings alfanuméricas não vazias, e o ano deve estar no intervalo de 0 até o ano atual.
     - UsuarioSchema: Valida o nome do usuário, que deve ser uma string alfanumérica não vazia.
     - IDSchema: Valida que o ID seja um número inteiro positivo.
   
2. Deserialização e Validação
   - O método `load()` do Marshmallow é usado para carregar os dados (converte JSON para Python) e 
   validá-los de acordo com as regras definidas nos schemas. 
   Se os dados não forem válidos, uma exceção `ValidationError` é lançada, e os erros são retornados na resposta.

3. exemplo de uso:
   livro_schema = utils.LivroSchema()
   try:
       livro = livro_schema.load(dados)   - Valida e carrega os dados
   except ValidationError as err:
       return jsonify({"erro": "Dados inválidos", "detalhes": err.messages}), 400 """


ano = datetime.now().year

def validar_alfanumerico(valor):
    if not re.match("^[A-Za-z0-9 ]+$", valor):
        raise ValidationError("O valor contém caracteres inválidos.")
    return valor

def validar_id(valor):
    
    if not valor:
        raise ValidationError("O ID não pode ser vazio")
    if not isinstance(valor, int) or valor <= 0:
        raise ValidationError("O ID deve ser um número inteiro positivo.")
    return valor


class LivroSchema(Schema):
    titulo = fields.String(required=True, validate=[validate.Length(min=1, error="O título não pode estar vazio."), validar_alfanumerico])
    autor = fields.String(required=True, validate=[validate.Length(min=1, error="O autor não pode estar vazio."), validar_alfanumerico])
    ano = fields.Integer(required=True, validate=validate.Range(min=0, max=ano, error="O ano deve ser entre 0 e ano atual."))

class UsuarioSchema(Schema):
    nome_usuario = fields.String(required=True, validate=[validate.Length(min=1, error="O nome do usuário não pode estar vazio"), validar_alfanumerico])

class IDSchema(Schema):
    id = fields.Integer(
        required = True,
        validate=[validar_id]
    )