from flask import Flask, render_template, request, redirect, url_for, session



app = Flask(__name__)
app.secret_key = 'patitoxd'


@app.before_request
def before_request():
    if 'inscritos' not in session:
        session['inscritos'] = []

@app.route('/')
def index():
    inscritos = session['inscritos']
    return render_template('index.html', inscritos=inscritos)

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nuevo_id = len(session['inscritos']) + 1
        inscrito = {
            'id': nuevo_id,
            'fecha': request.form['fecha'],
            'nombre': request.form['nombre'],
            'apellidos': request.form['apellidos'],
            'turno': request.form['turno'],
            'seminarios': ', '.join(request.form.getlist('seminarios'))
        }
        session['inscritos'].append(inscrito)
        session.modified = True
        return redirect(url_for('index'))
    return render_template('registro.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])

def editar(id):
    inscrito = next((i for i in session['inscritos'] if i['id'] == id), None)
    if request.method == 'POST':
        for inscrito in session['inscritos']:
            if inscrito['id'] == id:
                inscrito['nombre'] = request.form['nombre']
                inscrito['apellidos'] = request.form['apellidos']
                inscrito['turno'] = request.form['turno']
                inscrito['seminarios'] = ', '.join(request.form.getlist('seminarios'))
                session.modified = True
        return redirect(url_for('index'))
    return render_template('editar.html', inscrito=inscrito)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    session['inscritos'] = [i for i in session['inscritos'] if i['id'] != id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
