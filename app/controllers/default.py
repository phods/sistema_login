from bottle import route, run
from bottle import request, template
from bottle import static_file


from app import app



'''
@route('/')
@route('/user/<nome>')
def index(nome='Desconhecido'):
	return '<center><h1>Olá ' + nome + '</h1></center>'

@route('/artigo/<id>')
def artigo(id):
	return '<h1>Você está lendo o artigo ' + id + '</h1>'

@route('/pagina/<id>/<nome>')
def pagina(id, nome):
	return '<h1>Você está vendo a página ' + id + ' com o nome ' + nome + '</h1>'
'''

# static routes
@app.get('/<filename:re:.*\.css>')
def stylesheets(filename):
	return static_file(filename, root='static/css')

@app.get('/<filename:re:.*\.js>')
def javascripts(filename):
	return static_file(filename, root='static/js')

@app.get('/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
	return static_file(filename, root='static/img')

@app.get('/<filename:re:.*\.(eot|ttf|woff|svg)>')
def fonts(filename):
	return static_file(filename, root='static/fonts')

@app.route('/') # @get('/login')
def login():
	return template('login')

@app.route('/cadastro')
def cadastro():
	return template('cadastro')

@app.route('/cadastro',method='POST')
def acao_cadastro():
	username = request.forms.get('username')
	password = request.forms.get('password')
	insert_user(username,password)
	return template('verificacao_cadastro',nome=username)


'''
def check_login(username, password):
	d = {'marcos':'python', 'joao':'java', 'pedro':'go'}
	if username in d.keys() and d[username] == password:
		return True
	return False
'''

@app.route('/', method='POST') # @post('/login')
def acao_login():
	username = request.forms.get('username')
	password = request.forms.get('password')
	return template('verificacao_login', sucesso=check_login(username, password), nome=username)

@app.error(404)
def error404(error):
	return template('pagina404')