from bottle import route, run,request, template,redirect,static_file
from app.models.tables import User
from app import app
import bcrypt






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
def acao_cadastro(db,session):
	username = request.forms.get('username')
	
	
	try:
		db.query(User).filter(User.username==username).one()
		existe_username=True
		
	except:
		existe_username=False
	if not existe_username:
		password = request.forms.get('password')
		password_bytes=str.encode(password)
		salt_bytes=bcrypt.gensalt()
		salt=salt_bytes.decode()

		hashed_bytes=bcrypt.hashpw(password_bytes,salt_bytes)
		hashed=hashed_bytes.decode()

		new_user=User(username,hashed,salt)
		db.add(new_user)
		session['name']=username
		return redirect('/usuarios')

	return template('cadastro',existe_username=True)



@app.route('/', method='POST') # @post('/login')
def acao_login(db,session):
	username = request.forms.get('username')
	users=db.query(User).filter(User.username==username).all()
	
	if users:
		user=users[0]
		password = request.forms.get('password')
		password_bytes=str.encode(password)

		salt_bytes=str.encode(user.salt)
		hashed_bytes=bcrypt.hashpw(password_bytes,salt_bytes)
		hashed=hashed_bytes.decode()

		#result=bcrypt.checkpw(password_bytes,hashed_bytes)
		result = True if user.hashed ==  hashed else False
		if result:
			session['name']=username
			return redirect('/usuarios')
	
	#result=db.query(User).filter((User.username==username) & (User.password==password)).all()
	#sucesso = False if not result else True

	return template('login',sucesso=False)

@app.route('/usuarios')
def usuarios(db,session):
	if session.get('name'):
		acesso=True
	else:
		acesso=False

	userr=db.query(User).all()
	return template ('lista_usuarios',usuarios=userr,acesso=acesso)


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