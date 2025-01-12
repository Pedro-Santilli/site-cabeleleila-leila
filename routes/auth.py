from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import pandas as pd

auth_bp = Blueprint('auth', __name__)

def load_df_users():
    return pd.read_excel("database\\usuariosdb.xlsx")

def save_df_users(df):
    df.to_excel("database\\usuariosdb.xlsx", index=False)

@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        df = load_df_users()
        usuario = request.form['usuario']
        senha = request.form['senha']
        
        user = df[(df['usuario'] == usuario) & (df['senha'] == senha)]
        
        if not user.empty and usuario == "admin" and senha == "admin":
            return redirect(url_for('admin.ver_agendamentos_admin'))
        
        if not user.empty:
            session['usuario'] = usuario
            return redirect(url_for('agendamento.agendamento'))
        
        flash("Nome de usuário ou senha incorretos!", "login")
    return render_template("login.html")

@auth_bp.route("/cadastro", methods=["GET",'POST'])
def cadastrar():
    if request.method=="POST":
        df = load_df_users()
        usuario = request.form['usuario']
        senha = request.form['senha']
        email = request.form['email']
        
        conflito = df[(df['email'] == email)]
        if not conflito.empty:
            flash("Já existe um usuario com esse email.","cadastro")
            return render_template('cadastro.html')
        
        new_user = pd.DataFrame({
            'usuario': [usuario],
            'senha': [senha],
            'email': [email]
        })
        df = pd.concat([df, new_user], ignore_index=True)
        save_df_users(df)
        flash("Cadastro bem-sucedido! Agora você pode fazer login.","login")
        return redirect(url_for('auth.login'))
    return render_template("cadastro.html")