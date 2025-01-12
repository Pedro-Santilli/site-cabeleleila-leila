from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import pandas as pd

admin_bp = Blueprint('admin', __name__)

def load_df_service():
    df = pd.read_excel("database\\servico.xlsx")
    df['data'] = pd.to_datetime(df['data'], format='%Y-%m-%d', errors='coerce').dt.strftime('%Y-%m-%d')
    return df

def save_df_service(df):
    df.to_excel("database\\servico.xlsx", index=False)

@admin_bp.route('/ver-agendamentos-admin')
def ver_agendamentos_admin():
    df = load_df_service()
    data = df.to_dict(orient='records')
    return render_template('ver_agendamentos_admin.html', data=data)

@admin_bp.route('/edit-admin')
def edit_admin():
    usuario = request.args.get('usuario')
    data = request.args.get('data')
    horario = request.args.get('horario')
    
    df = load_df_service()
    row = df[(df['usuario'] == usuario) & (df['data'] == data) & (df['horario'] == horario)].iloc[0]
    return render_template('edit_admin.html', row=row)

@admin_bp.route('/edit-admin', methods=["POST"])
def editar_admin():
    usuario = request.form['usuario']
    data_antiga = request.form['data_antiga']
    horario_antigo = request.form['horario_antigo']
    nova_data = request.form['nova_data']
    novo_horario = request.form['novo_horario']
    df = load_df_service()
    registro_a_editar = df[(df['usuario'] == usuario) & (df['data'] == data_antiga) & (df['horario'] == horario_antigo)]
    if registro_a_editar.empty:
        flash("Agendamento não encontrado.", "editar")
        return redirect(url_for('admin.ver_agendamentos_admin'))
    df.loc[(df['usuario'] == usuario) & (df['data'] == data_antiga) & (df['horario'] == horario_antigo), ['data', 'horario']] = [nova_data, novo_horario]
    save_df_service(df)
    flash("Agendamento editado com sucesso.", "editar")
    return redirect(url_for('admin.ver_agendamentos_admin'))