from flask import Flask, render_template

app = Flask(__name__)

# rota principal (home)
@app.route('/')
def home():
    return render_template('index.html')

# rota sobre 
@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

# rota dos cursos
@app.route('/cursos')
def cursos():
    return render_template('cursos.html')

@app.route('/campus')
def campus():
    return render_template('campus.html')

<<<<<<< HEAD
if __name__ == '__main__':
    app.run(debug=True)
=======
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

if __name__ == '__main__':
    app.run(debug=True)


>>>>>>> 399f637 (páginas de cursos + melhorias (Evelyn))
