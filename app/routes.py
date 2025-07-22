# routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from app import db, bcrypt
from app.models import User, Reuniao, Presenca
from app.forms import LoginForm, CadastroForm
import os

main = Blueprint('main', __name__)

UPLOAD_FOLDER = 'app/static/uploads'

@main.route('/')
def home():
    return redirect(url_for('main.login'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.senha, form.senha.data):
            login_user(user)
            if user.is_admin:
                return redirect(url_for('main.admin'))
            else:
                return redirect(url_for('main.painel'))
        else:
            flash('E-mail ou senha incorretos.', 'danger')
    return render_template('login.html', form=form)

@main.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    form = CadastroForm()
    if form.validate_on_submit():
        filename = None
        if form.foto.data:
            filename = secure_filename(form.foto.data.filename)
            form.foto.data.save(os.path.join(UPLOAD_FOLDER, filename))

        hashed_pw = bcrypt.generate_password_hash(form.senha.data).decode('utf-8')
        novo_user = User(
            nome=form.nome.data,
            email=form.email.data,
            senha=hashed_pw,
            celular=form.celular.data,
            idade=form.idade.data,
            tabor_feito=form.tabor_feito.data,
            foto=filename
        )
        db.session.add(novo_user)
        db.session.commit()
        flash('Cadastro realizado com sucesso! Faça login.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route('/painel')
@login_required
def painel():
    reunioes = Reuniao.query.all()
    presencas = [p.reuniao_id for p in Presenca.query.filter_by(user_id=current_user.id).all()]
    return render_template('painel.html', nome=current_user.nome, reunioes=reunioes, presencas=presencas)

@main.route('/marcar_presenca/<int:reuniao_id>')
@login_required
def marcar_presenca(reuniao_id):
    existente = Presenca.query.filter_by(user_id=current_user.id, reuniao_id=reuniao_id).first()
    if not existente:
        nova = Presenca(user_id=current_user.id, reuniao_id=reuniao_id)
        db.session.add(nova)
        db.session.commit()
    return redirect(url_for('main.painel'))

@main.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        return redirect(url_for('main.painel'))
    usuarios = User.query.all()
    reunioes = Reuniao.query.all()
    return render_template('admin.html', usuarios=usuarios, reunioes=reunioes)

@main.route('/admin/remover_usuario/<int:user_id>')
@login_required
def remover_usuario(user_id):
    if not current_user.is_admin:
        return redirect(url_for('main.painel'))
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('main.admin'))

@main.route('/admin/adicionar_reuniao', methods=['POST'])
@login_required
def adicionar_reuniao():
    if not current_user.is_admin:
        return redirect(url_for('main.painel'))
    data = request.form.get('data')
    tema = request.form.get('tema')
    if data and tema:
        nova = Reuniao(data=data, tema=tema)
        db.session.add(nova)
        db.session.commit()
    return redirect(url_for('main.admin'))