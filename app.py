
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import date

app = Flask(__name__)
app.secret_key = 'campusvirtualifrn'


def conectar_banco():
    return sqlite3.connect('vagas.db')


def vagas_do_curso(curso):
    banco = conectar_banco()
    cursor = banco.cursor()

    cursor.execute('''
        SELECT * FROM vagas
        WHERE curso = ?
    ''', (curso,))

    vagas = cursor.fetchall()
    banco.close()

    return vagas


def criar_tabelas():
    banco = conectar_banco()
    cursor = banco.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS empresas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vagas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa TEXT NOT NULL,
            titulo TEXT NOT NULL,
            descricao TEXT NOT NULL,
            requisitos TEXT NOT NULL,
            contato TEXT NOT NULL,
            data_inicio TEXT NOT NULL,
            data_fim TEXT NOT NULL,
            curso TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS curriculos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            curso TEXT NOT NULL,
            experiencia TEXT NOT NULL,
            vaga_id INTEGER,
            FOREIGN KEY (vaga_id) REFERENCES vagas(id)
        )
    ''')

    banco.commit()
    banco.close()


criar_tabelas()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/sobre')
def sobre():
    return render_template('sobre.html')


@app.route('/campus')
def campus():
    return render_template('campus.html')


@app.route('/curso/informatica')
def curso_informatica():
    vagas = vagas_do_curso('Informática para Internet')

    return render_template(
        'curso_informatica.html',
        vagas=vagas
    )


@app.route('/curso/textil')
def curso_textil():
    vagas = vagas_do_curso('Têxtil')

    return render_template(
        'curso_textil.html',
        vagas=vagas
    )


@app.route('/curso/vestuario')
def curso_vestuario():
    vagas = vagas_do_curso('Vestuário')

    return render_template(
        'curso_vestuario.html',
        vagas=vagas
    )


@app.route('/curso/eletrotecnica')
def curso_eletro():
    vagas = vagas_do_curso('Eletrotécnica')

    return render_template(
        'curso_eletrotecnica.html',
        vagas=vagas
    )


@app.route('/cadastro-empresa', methods=['GET', 'POST'])
def cadastro_empresa():

    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        banco = conectar_banco()
        cursor = banco.cursor()

        cursor.execute(
            'SELECT * FROM empresas WHERE email = ?',
            (email,)
        )

        empresa_existente = cursor.fetchone()

        if empresa_existente:
            banco.close()

            return render_template(
                'cadastro_empresa.html',
                erro='Este e-mail já está cadastrado.'
            )

        cursor.execute('''
            INSERT INTO empresas
            (nome, email, senha)
            VALUES (?, ?, ?)
        ''', (nome, email, senha))

        banco.commit()
        banco.close()

        return redirect('/login')

    return render_template('cadastro_empresa.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        banco = conectar_banco()
        cursor = banco.cursor()

        cursor.execute('''
            SELECT * FROM empresas
            WHERE email = ? AND senha = ?
        ''', (email, senha))

        empresa = cursor.fetchone()
        banco.close()

        if empresa:
            session['empresa_id'] = empresa[0]
            session['empresa_nome'] = empresa[1]

            return redirect('/vagas')

        return render_template(
            'login.html',
            erro='Empresa não encontrada. Faça seu cadastro primeiro.'
        )

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/vagas')
def vagas():
    banco = conectar_banco()
    cursor = banco.cursor()

    cursor.execute('SELECT * FROM vagas')
    vagas = cursor.fetchall()

    banco.close()

    return render_template('vagas.html', vagas=vagas)


@app.route('/editar-vaga/<int:id>', methods=['GET', 'POST'])
def editar_vaga(id):

    banco = conectar_banco()
    cursor = banco.cursor()

    if request.method == 'POST':

        empresa = request.form['empresa']
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        curso = request.form['curso']
        requisitos = request.form['requisitos']
        contato = request.form['contato']

        cursor.execute('''
            UPDATE vagas
            SET empresa = ?,
                titulo = ?,
                descricao = ?,
                curso = ?,
                requisitos = ?,
                contato = ?
            WHERE id = ?
        ''', (
            empresa,
            titulo,
            descricao,
            curso,
            requisitos,
            contato,
            id
        ))

        banco.commit()
        banco.close()

        return redirect(url_for('vagas'))

    cursor.execute(
        'SELECT * FROM vagas WHERE id = ?',
        (id,)
    )

    vaga = cursor.fetchone()

    banco.close()

    return render_template(
        'editar_vaga.html',
        vaga=vaga
    )


@app.route('/excluir-vaga/<int:id>')
def excluir_vaga(id):

    banco = conectar_banco()
    cursor = banco.cursor()

    cursor.execute(
        'DELETE FROM vagas WHERE id = ?',
        (id,)
    )

    banco.commit()
    banco.close()

    return redirect(url_for('vagas'))


@app.route('/cadastrar-vaga', methods=['GET', 'POST'])
def cadastrar_vaga():

    if 'empresa_id' not in session:
        return redirect('/login')

    if request.method == 'POST':

        empresa = session['empresa_nome']
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        requisitos = request.form['requisitos']
        contato = request.form['contato']
        data_inicio = request.form['data_inicio']
        data_fim = request.form['data_fim']
        curso = request.form['curso']

        banco = conectar_banco()
        cursor = banco.cursor()

        cursor.execute('''
            INSERT INTO vagas
            (empresa, titulo, descricao, requisitos, contato, data_inicio, data_fim, curso)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            empresa,
            titulo,
            descricao,
            requisitos,
            contato,
            data_inicio,
            data_fim,
            curso
        ))

        banco.commit()
        banco.close()

        return redirect(url_for('vagas'))

    hoje = date.today().isoformat()

    return render_template(
        'cadastrar_vaga.html',
        hoje=hoje,
        empresa=session['empresa_nome']
    )


if __name__ == '__main__':
    app.run(debug=True)

