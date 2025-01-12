from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import pandas as pd
from datetime import datetime, timedelta

agendamento_bp = Blueprint('agendamento', __name__)

def load_df_service():
    df = pd.read_excel("database\\servico.xlsx")
    df['data'] = pd.to_datetime(df['data'], format='%Y-%m-%d', errors='coerce').dt.strftime('%Y-%m-%d')
    return df

def save_df_service(df):
    df.to_excel("database\\servico.xlsx", index=False)

@agendamento_bp.route('/agendamento')
def agendamento():
    return render_template("agendamento.html")

@agendamento_bp.route('/agendamento', methods=['POST'])
def efetuar_agendamento():
    df = load_df_service()
    horario = request.form["horario"]
    data = request.form["data"]
    servico = request.form["servico"]
    usuario = session['usuario']
    
    try:
        data_agendamento = datetime.strptime(data, '%Y-%m-%d')
    except ValueError:
        flash("Formato de data inválido. Use o formato YYYY-MM-DD.", "agendamento")
        return redirect(url_for('agendamento.agendamento'))
    
    inicio_semana = data_agendamento - timedelta(days=data_agendamento.weekday())
    fim_semana = inicio_semana + timedelta(days=6)
    
    agendamentos_semana = df[(df['usuario'] == usuario) & 
                             (pd.to_datetime(df['data'], format='%Y-%m-%d', errors='coerce') >= inicio_semana) & 
                             (pd.to_datetime(df['data'], format='%Y-%m-%d', errors='coerce') <= fim_semana)]
    
    if 'tentativas' not in session:
        session['tentativas'] = 0

    if not agendamentos_semana.empty and session['tentativas'] < 1:
        data_existente = agendamentos_semana.iloc[0]['data']
        flash(f"Você já tem um agendamento nesta semana. Que tal agendar para o mesmo dia ({data_existente})?", "agendamento")
        session['tentativas'] += 1  
        return redirect(url_for('agendamento.agendamento'))
    
    conflito = df[(df['data'] == data) & (df['horario'] == horario)]
    if not conflito.empty:
        flash("Já existe um agendamento para essa data e horário.","agendamento")
        return redirect(url_for('agendamento.agendamento'))
    
    new_servico = pd.DataFrame({
            "usuario" : [usuario],
            "data"    : [data],
            "horario" : [horario],
            "servico" : [servico]
        })
    df = pd.concat([df, new_servico], ignore_index=True)
    save_df_service(df)
    flash("Agendamento realizado com sucesso!","agendamento")
    return redirect(url_for('agendamento.agendamento'))

@agendamento_bp.route('/ver-agendamentos')
def ver_agendamentos():
    df = load_df_service()
    admin_df = df[df['usuario'] == session["usuario"]]
    
    data = admin_df.to_dict(orient='records')
    return render_template('ver_agendamentos.html', data=data)

@agendamento_bp.route('/edit')
def edit():
    usuario = session["usuario"]
    data = request.args.get('data')
    horario = request.args.get('horario')
    
    df = load_df_service()
    admin_df = df[df['usuario'] == usuario]
    
    row = admin_df[(admin_df['data'] == data) & (admin_df['horario'] == horario)].iloc[0]
    
    today = datetime.now().date()
    try:
        agendamento_data = datetime.strptime(row['data'], '%Y-%m-%d').date()
    except ValueError:
        flash("Formato de data inválido no agendamento.", "erro")
        return redirect(url_for('agendamento.ver_agendamentos'))
    
    if agendamento_data <= today + timedelta(days=2):
        flash("Você só pode editar agendamentos com mais de dois dias de antecedência.", "editar")
        return redirect(url_for('agendamento.ver_agendamentos'))
    return render_template('edit.html', row=row)

@agendamento_bp.route('/edit', methods=["POST"])
def editar():
    usuario = session["usuario"]
    data_antiga = request.form['data_antiga']
    horario_antigo = request.form['horario_antigo']
    nova_data = request.form['nova_data']
    novo_horario = request.form['novo_horario']
    df = load_df_service()
    admin_df = df[df['usuario'] == usuario]
    registro_a_editar = admin_df[(admin_df['data'] == data_antiga) & (admin_df['horario'] == horario_antigo)]
    if registro_a_editar.empty:
        flash("Agendamento não encontrado.", "editar")
        return redirect(url_for('agendamento.ver_agendamentos'))
    today = datetime.now().date()
    try:
        agendamento_data = datetime.strptime(registro_a_editar['data'].values[0], '%Y-%m-%d').date()
    except ValueError:
        flash("Formato de data inválido no agendamento.", "erro")
        return redirect(url_for('agendamento.ver_agendamentos'))
    
    if agendamento_data <= today + timedelta(days=2):
        flash("Você só pode editar agendamentos com mais de dois dias de antecedência.", "editar")
        return redirect(url_for('agendamento.ver_agendamentos'))
    df.loc[(df['usuario'] == usuario) & (df['data'] == data_antiga) & (df['horario'] == horario_antigo), ['data', 'horario']] = [nova_data, novo_horario]
    save_df_service(df)
    flash("Agendamento editado com sucesso.", "editar")
    return redirect(url_for('agendamento.ver_agendamentos'))