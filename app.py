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

if __name__ == '__main__':
    app.run(debug=True)