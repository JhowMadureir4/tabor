from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_wtf.file import FileAllowed

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')

class CadastroForm(FlaskForm):
    foto = FileField('Foto', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Somente imagens!')])
    nome_completo = StringField('Nome completo', validators=[DataRequired(), Length(min=3)])
    celular = StringField('Número de celular', validators=[DataRequired(), Length(min=9, max=20)])
    idade = IntegerField('Idade', validators=[DataRequired()])
    tabor = StringField('Qual Tabor fez', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    confirmar_senha = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('senha')])
    submit = SubmitField('Concluir Cadastro')