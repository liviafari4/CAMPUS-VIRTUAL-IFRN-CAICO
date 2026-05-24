from flask import Flask, render_template, request, redirect, url_for
import sqlite3
app = Flask(__name__)


def conectar_banco():
    return sqlite3.connect('vagas.db')


def criar_tabelas():
    banco = conectar_banco()
    cursor = banco.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vagas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa TEXT NOT NULL,
            titulo TEXT NOT NULL,
            descricao TEXT NOT NULL,
            requisitos TEXT NOT NULL,
            contato TEXT NOT NULL
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

@app.route('/cursos')
def cursos():
    return render_template('cursos.html')

@app.route('/campus')
def campus():
    return render_template('campus.html')

@app.route('/curso/informatica')
def curso_informatica():
    return render_template('curso_informatica.html')

@app.route('/curso/textil')
def curso_textil():
    return render_template('curso_textil.html')

@app.route('/curso/vestuario')
def curso_vestuario():
    return render_template('curso_vestuario.html')

@app.route('/curso/eletrotecnica')
def curso_eletro():
    return render_template('curso_eletrotecnica.html')


@app.route('/vagas')
def vagas():
    banco = conectar_banco()
    cursor = banco.cursor()

    cursor.execute('SELECT * FROM vagas')
    vagas = cursor.fetchall()

    banco.close()

    return render_template('vagas.html', vagas=vagas)


@app.route('/cadastrar-vaga', methods=['GET', 'POST'])
def cadastrar_vaga():
    if request.method == 'POST':
        empresa = request.form['empresa']
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        requisitos = request.form['requisitos']
        contato = request.form['contato']

        banco = conectar_banco()
        cursor = banco.cursor()

        cursor.execute('''
            INSERT INTO vagas (empresa, titulo, descricao, requisitos, contato)
            VALUES (?, ?, ?, ?, ?)
        ''', (empresa, titulo, descricao, requisitos, contato))

        banco.commit()
        banco.close()

        return redirect(url_for('vagas'))

    return render_template('cadastrar_vaga.html')


@app.route('/enviar-curriculo/<int:vaga_id>', methods=['GET', 'POST'])
def enviar_curriculo(vaga_id):
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        curso = request.form['curso']
        experiencia = request.form['experiencia']

        banco = conectar_banco()
        cursor = banco.cursor()

        cursor.execute('''
            INSERT INTO curriculos (nome, email, curso, experiencia, vaga_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (nome, email, curso, experiencia, vaga_id))

        banco.commit()
        banco.close()

        return redirect(url_for('vagas'))

    return render_template('enviar_curriculo.html', vaga_id=vaga_id)

    
if __name__ == '__main__':
    app.run(debug=True)
