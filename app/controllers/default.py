from bottle import route, run,request, template,redirect,static_file

from app.models.tables import User

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
	return static_file(filename, root='app/static/css')

@app.get('/<filename:re:.*\.js>')
def javascripts(filename):
	return static_file(filename, root='app/static/js')

@app.get('/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
	return static_file(filename, root='app/static/img')

@app.get('/<filename:re:.*\.(eot|ttf|woff|svg)>')
def fonts(filename):
	return static_file(filename, root='app/static/fonts')

@app.route('/') # @get('/login')
def login():
	return template('login',sucesso=True)

@app.route('/cadastro')
def cadastro():
	return template('cadastro',existe_username=False)

@app.route('/cadastro',method='POST')
def acao_cadastro(db):
	
	

	username = request.forms.get('username')
	password = request.forms.get('password')
	try:
		db.query(User).filter(User.username==username).one()
		existe_username=True
		
	except:
		existe_username=False
	if not existe_username:
		new_user=User(username,password)
		db.add(new_user)
		return redirect('/usuarios')

	return template('cadastro',existe_username=True)



@app.route('/', method='POST') # @post('/login')
def acao_login(db):
	username = request.forms.get('username')
	password = request.forms.get('password')
	result=db.query(User).filter((User.username==username) & (User.password==password)).all()
	#sucesso = False if not result else True
	if result:
		return redirect('/usuarios')
	return template('login',sucesso=False)

@app.route('/usuarios')
def usuarios(db):
	userr=db.query(User).all()
	return template ('lista_usuarios',usuarios=userr)


@app.error(404)
def error404(error):
	return template('pagina404')


'''
def check_login(username, password):
	d = {'marcos':'python', 'joao':'java', 'pedro':'go'}
	if username in d.keys() and d[username] == password:
		return True
	return False
'''