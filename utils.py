import re
from marshmallow import Schema, fields, validate, ValidationError
from datetime import datetime

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