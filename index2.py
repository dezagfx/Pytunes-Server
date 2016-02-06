# /usr/bin/env python
import bottle
from bottle import (route, response, run, redirect, request, static_file,
                    ServerAdapter, default_app, template, error, hook, abort)
import json
from config import config
# from database.models import User, Music, Playlist, UserSession
from lib import json_response as jresp, auth
import re
from sqlalchemy import (Table, Column, Integer, String, MetaData, ForeignKey,
                        Sequence)
# from sqlalchemy.orm import Query
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import text
from sqlalchemy import create_engine
# from database import config as db_conf


# Adicionar o caminho completo para a localizaçao das views
# Deveria funcionar por defeito, mas por alguma razao tem de ser explicito
bottle.TEMPLATE_PATH.insert(0, config.base_path + '/views/')
###############################################################################
# Servidor de Base de Dados:
###############################################################################
db_user = 'pytunes'
db_name = 'pytunes'
db_host = '178.79.165.224'
db_pass = 'Lmxy20#a'
db_port = '3306'

###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################


@hook('before_request')
def before_request():
    '''
    # print(bottle.default_app().routes)
    # bottle.py linha 612
    for r in bottle.default_app().routes:
        print(r.rule)
    '''

    '''
    # Caminhos livremente acessiveis:
    no_auth_paths = ('/', '/docs')
    # Prefixos de caminhos livremente acessiveis:
    no_auth_path_prefixes = ('assets')
    # http://bottlepy.org/docs/dev/api.html#the-request-object
    full_path = bottle.request.fullpath
    path_prefix = bottle.request.fullpath.split('/')[1]
    # Caso para a rota seja preciso autenticaçao:
    if (full_path not in no_auth_paths
        and path_prefix not in no_auth_path_prefixes):
        from services import auth
        if not auth.is_authenticated(request):
            # abort(): bottle.py linha 2457
            # Levanta uma excepç~ao HTTPError definida em bottle.py linha 1811
            abort(403, auth.auth_error)
    '''

    # Qual o ip base / url base? Em vez de termos este valor 'hard coded'
    # detectamo-lo para cada pedido (permite alternar entre ip's facilmente)

    # O parametro 'Host' do header pode ser manipulado e, regra geral, nao e
    # boa ideia confiar, mas aqui vamos usa-lo de forma a podermos detectar
    # dinamicamente o ip
    http_host = bottle.request.get_header('host')
    global base_url
    base_url = 'https://' + http_host + '/'
    global assets_base_url
    assets_base_url = base_url + 'assets/'
    
    # E necessario re-iniciar a 'connection' a cada request, e tornar a varivel
    # global devido a cache do sqlalchemy 
    connection_string = str(
        'mysql+pymysql://' + db_user + ':' + db_pass + '@' + db_host + '/' +
        db_name
        )
    engine = create_engine(connection_string, echo=False)
    global connection
    connection = engine.connect()


    # global token
    # token = bottle.request.forms.get('token')


metadata = MetaData()


class User():

    table = Table(
        'users',
        metadata,
        Column('id', Integer, Sequence('user_id_seq'), primary_key=True),
        Column('name', String(255)),
        Column('email', String(255)),
        Column('password', String(255)),
    )


    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def save(self):
        s = self.table.insert().values(
                name=self.name,
                email=self.email,
                password=self.password,
            )
        connection.execute(s)

    @staticmethod
    def get_by_id(user_id):
        s = User.table.select().where(User.table.c.id == user_id)
        return connection.execute(s).fetchone()

    @staticmethod
    def get_by_name(name):
        s = User.table.select().where(User.table.c.name == name)
        return connection.execute(s).fetchone()

    @staticmethod
    def get_by_email(email):
        s = User.table.select().where(User.table.c.email == email)
        return connection.execute(s).fetchone()


class Music():

    table = Table(
        'musics',
        metadata,
        Column('id', Integer, Sequence('session_id_seq'), primary_key=True),
        Column('name', String(255)),
        Column('file_name', String(255)),
        Column('user_id',  None, ForeignKey('users.id')),
    )

    def __init__(self, name, file_name, user_id):
        self.name = name
        self.file_name = file_name
        self.user_id = user_id

    def save(self):
        s = self.table.insert().values(
                name=self.name,
                file_name=self.file_name,
                user_id=self.user_id,
            )
        connection.execute(s)

    @staticmethod
    def get_all():
        s = Music.table.select()
        return connection.execute(s).fetchall()

    @staticmethod
    def get_file_name_by_id(music_id):
        s = Music.table.select().where(Music.table.c.id == music_id)
        result = connection.execute(s).fetchall()
        try:
            return result['file_name']
        except:
            return False

    @staticmethod
    def get_all_by_user_id(user_id):
        s = Music.table.select().where(Music.table.c.user_id == user_id)
        return connection.execute(s).fetchall()

    @staticmethod
    def get_all_by_playlist_id(playlist_id):
        s = text('''
        SELECT
            musics.*
        FROM
            musics
        INNER JOIN
            musics_playlists on musics.id = musics_playlists.music_id
        WHERE
            musics_playlists.playlist_id = :playlist_id
        ORDER BY
            musics_playlists.music_order
            ''')

        return connection.execute(s, playlist_id=int(playlist_id)).fetchall()
        '''
        print names
        s = Music.table.select().where(Music.table.c.user_id == user_id)
        return connection.execute(s).fetchall()

        result = connection.execute(sql)
        names = []
        for row in result:
            names.append(row[0])
        '''


class Playlist():

    table = Table(
        'playlists',
        metadata,
        Column('id', Integer, Sequence('playlist_id_seq'), primary_key=True),
        Column('name', String(255)),
        Column('user_id', None, ForeignKey('users.id')),
    )

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id

    def save(self):
        s = self.table.insert().values(
                name=self.name,
                user_id=self.user_id,
            )
        connection.execute(s)

    @staticmethod
    def get_all_by_user_id(user_id):
        s = Playlist.table.select().where(Playlist.table.c.user_id == user_id)
        return connection.execute(s).fetchall()


class UserSession():

    table = Table(
        'user_sessions',
        metadata,
        Column('id', Integer, Sequence('session_id_seq'), primary_key=True),
        Column('user_id',  Integer, ForeignKey('users.id')),
        Column('token', String(255)),
    )

    def __init__(self, user_id, token):
        self.user_id = user_id
        self.token = token

    def save(self):
        s = self.table.insert().values(
                user_id=self.user_id,
                token=self.token,
            )
        connection.execute(s)

    @staticmethod
    def delete_session(token):
        s = UserSession.table.delete(). \
            where(UserSession.table.c.token == token)
        connection.execute(s)

    @staticmethod
    def token_exists(token):
        s = UserSession.table.select(). \
            where(UserSession.table.c.token == token)
        if connection.execute(s).fetchone() != None:
            return True
        return False

    @staticmethod
    def get_user_id_by_token(token):
        # Assumimos que o user_id tem de estar SEMPRE definido
        s = UserSession.table.select(UserSession.table.c.user_id). \
            where(UserSession.table.c.token == token)
        result = connection.execute(s).fetchone()
        return result.user_id



###############################################################################
error_message = {
                'success': False,
                'message': []
            }


@error(404)
def error404(error):
    return 'Caminho nao encontrado'


@error(405)
def error405(error):
    return 'Metodo nao permitido'


@error(403)
def error403(error):
    response.set_header('Content-Type', 'application/json; charset=UTF-8')
    return json.dumps(error.body)


@route('/assets/<filepath:path>')
def server_static(filepath):
    # Roteamento de ficheiros estaticos
    # http://bottlepy.org/docs/dev/tutorial.html#routing-static-files
    return static_file(filepath, root=config.base_path+'/assets')


@route('/musics/<filepath:path>')
def static_mp3(filepath):
    # filepath = Music.get_file_name_by_id(music_id)
    # Roteamento de ficheiros estaticos
    # http://bottlepy.org/docs/dev/tutorial.html#routing-static-files
    return static_file(filepath, root=config.base_path+'/musics')

###############################################################################


@route('/', method='GET')
def index():
    # print('base_path->', base_path)
    # return base_url
    # return bottle.request.get_header('host')
    # userName = request.query.userName
    """
    userName = request.forms.get('userName')
    password = request.forms.get('password')

    print(password)
    print(userName)

    if userName == 'ruben' and password == '1234':
        return template('Sucesso: Ola {{!name}}', name=userName)
    return 'erro: Poe-te nas putas'
    """
    view_data = {
        'base_url': base_url,
        'assets_base_url': assets_base_url
    }
    return template('email/account_activation', **view_data)


@route('/docs', method='GET')
def docs():
    view_data = {
        'base_url': base_url,
        'assets_base_url': assets_base_url
    }
    # template('I live at {{number}} {{street}}, {{city}}', **view_data)
    return template('docs/index', **view_data)

###############################################################################
# Autenticaç~ao
###############################################################################


@route('/auth/login', method='POST')
def auth_login():

    error_message = []

    user_name = request.forms.get('user_name')
    input_password = request.forms.get('password')

    u = User.get_by_name(user_name)
    print(u)

    # O utilizador nao existe?
    # if u is None or auth.password_matches(input_password, u['password']):
    if u is None:
        error_message.append('Credenciais incorrectas')
    if user_name == '':
        error_message.append('O nome de utilizador esta vazio')
    if input_password == '':
        error_message.append('O campo password esta vazio')
    if len(error_message) > 0:
        return jresp.reply(
                payload=None,
                success=False,
                error_message=error_message
            )
    else:
        db_password = u['password']

        # Validar palavra-passe
        if not auth.password_matches(input_password, db_password):
            error_message.append('Credenciais incorrectas')
            return jresp.reply(
                    payload=None,
                    success=False,
                    error_message=error_message
                )
        # User existe e password esta correcta:
        # criar e gravar token de sessao
        # enviar mensagem com o token de sessao

        new_session_token = auth.generate_session_token()

        new_session = UserSession(
                user_id=u['id'],
                token=new_session_token
            )
        new_session.save()

        # Tudo correu bem:
        payload = {
                'token': new_session_token
                }
        return jresp.reply(
                payload=payload,
                error_message=None,
                success=True
            )


@route('/auth/logout', method='GET')
def auth_logout():

    token = request.forms.get('token')

    if not UserSession.token_exists(token):
        error_message.append('A sessao nao existe')
        return jresp.reply(
                payload=None,
                success=False,
                error_message=error_message
            )
    else:
        UserSession.delete_session(token)


@route('/auth/check_token', method='POST')
def check_token():
    token = request.forms.get('token')

    if UserSession.token_exists(token):

        user_id = UserSession.get_user_id_by_token(token)
        user = User.get_by_id(user_id)

        payload = {
                'message': 'A sessao encontra-se activa.',
                'user': {
                    'name': user.name,
                }
                }
        return jresp.reply(
                payload=payload,
                )
    else:
        error_message = [['A sessao nao esta activa']]
        return jresp.reply(
                payload=None,
                success=False,
                error_message=error_message
            )


@route('/auth/create_account', method='POST')
def create_account():
    print('create account')
    error_message = []

    name = request.forms.get('name', '')
    password = request.forms.get('password', '')
    password_confirmation = request.forms.get('password_confirmation', '')
    email = request.forms.get('email', '')
    print('1')
    # Validaçao:
    if name == '':
        error_message.append('O nome de Utilizador esta vazio')
    if password == '':
        error_message.append('O campo password esta vazio')
    if password is not None and len(password) > 6:
        error_message.append('A password tem de ter pelo menos 6 caracteres')
    if password_confirmation == '':
        error_message.append('O campo confirmaçao de password esta vazio')
    if password != password_confirmation:
        error_message.append('As passwords nao sao iguais')
    print('3')
    # http://stackoverflow.com/questions/8022530/
    # python-check-for-valid-email-address/8022584#8022584
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        error_message.append('O endereço de email nao e valido')
    print('4')
    # Ja existe algum utilizador na base de dados com este nome?
    if name != '':
        u = User.get_by_name(name)
        if u is not None:
            error_message.append('O nome de utilizador ja existe')
    # Ja existe algum utilizador na base de dados com este Email?
    if email != '':
        u = User.get_by_email(email)
        if u is not None:
            error_message.append('O email ja existe')
    print('5')
    # Alguma das Validaç~oes devolveu erro?
    if len(error_message) > 0:
        return jresp.reply(
                payload=None,
                success=False,
                error_message=error_message
            )
    else:
        # 1->Inserir o novo utilizador
        # 2->Enviar o email
        plaintext_password = password
        hashed_password = auth.hash_password(plaintext_password)

        try:
            user = User(name=name, email=email, password=hashed_password)
            user.save()
        except:
            error_message.append('Erro ao comunicar com a base de dados!')
            return jresp.reply(
                    response=response,
                    payload=None,
                    success=False,
                    error_message=error_message,
                    status=500
                )
        '''
        from services import mailgun as mail
        try:
            mail.send(template='account_confirmation', name=name, email=email)
        except:
            error_message.append('Erro ao enviar email!')
            return jresp.reply(
                    response=response,
                    payload=None,
                    success=False,
                    error_message=error_message
                )
        '''
        # Tudo correu bem:
        payload = [{
                'message': 'Conta de utilizador criada com sucesso.'
                }]

        return jresp.reply(
                payload=payload,
                )


@route('/auth/recover_account', method='GET')
def recover_account():
    error_message = []
    email = request.query.get('email', '')

###############################################################################


@route('/user/playlists', method='GET')
def get_playlists_by_user():

    token = request.forms.get('token')
    user_id = UserSession.get_user_id_by_token(token)
    playlists = Playlist.get_all_by_user_id(user_id)

    payload = {'playlists': []}

    for playlist in playlists:
        p = {'id': playlist.id, 'name': playlist.name}
        payload['playlists'].append(p)

    return jresp.reply(
            payload=payload,
            error_message=None,
            success=True
        )


@route('/playlists/<id>')
def playlists(id):
    musics_in_playlist = Music.get_all_by_playlist_id(id)

    payload = {'musics': []}

    for m in musics_in_playlist:
        music = {'id': m['id'], 'name': m['name'], 'file_name': m['file_name']}
        payload['musics'].append(music)

    return jresp.reply(
            payload=payload,
            error_message=None,
            success=True
        )


@route('/playlists/add', method='POST')
def playlists_add():
    token = request.forms.get('token')
    user_id = UserSession.get_user_id_by_token(token)

    playlist_name = request.forms.get('playlist_name')

    playlist = Playlist(name=playlist_name, user_id=user_id)
    playlist.save()

    payload = {'message': ['Playlist adicionada com sucesso']}

    return jresp.reply(
            payload=payload,
            error_message=None,
            success=True
        )


@route('/musics/', method='GET')
def musics():
    token = request.forms.get('token')

    musics = Music.get_all()

    payload = {'musics': []}

    for music in musics:
        m = {'id': music.id, 'name': music.name, 'file_name': music.file_name}
        payload['musics'].append(m)

    return jresp.reply(
            payload=payload,
            error_message=None,
            success=True
        )



@route('/test/')
def test():
    # dicc = parse_qs(request.query_string)
    # print(request.query_string)´
    # qs = request.query_string
    # print(request.query.decode())
    for key, value in request.query.decode().items():
        print(key, '->', value)


###############################################################################

# Copiado e adaptado de:
# http://www.socouldanyone.com/2014/01/bottle-with-ssl.html
if config.server_type == 'SSLWSGIRefServer':
    class SSLWSGIRefServer(ServerAdapter):
        def run(self, handler):
            from wsgiref.simple_server import (make_server,
                                               WSGIRequestHandler)
            import ssl
            if self.quiet:
                class QuietHandler(WSGIRequestHandler):
                    def log_request(*args, **kw): pass
                self.options['handler_class'] = QuietHandler
            srv = make_server(
                    self.host, self.port, handler, **self.options
                )
            srv.socket = ssl.wrap_socket(
                srv.socket,
                # caminho para o certificado
                certfile=config.serverCertPem,
                # caminho para a chave privada
                keyfile=config.serverCertKey,
                server_side=True)
            srv.serve_forever()

    """
    Daqui inicializamos o servidor que herda do ServerAdapter da framwork
    passando para o construtor (bottle.py linha 2782) o host e a porta
    """
    srv = SSLWSGIRefServer(
            host=config.host,
            port=config.server_port,
        )

    run(server=srv, reloader=config.auto_reload)


'''
###############################################################################
# Create our own sub-class of Bottle's ServerAdapter
# so that we can specify SSL. Using just server='cherrypy'
# uses the default cherrypy server, which doesn't use SSL
class SSLCherryPyServer(ServerAdapter):
    def run(self, handler):
        from cherrypy import wsgiserver
        from cherrypy.wsgiserver.ssl_pyopenssl import pyOpenSSLAdapter
        server = wsgiserver.CherryPyWSGIServer((self.host, self.port), handler)
        server.ssl_adapter = pyOpenSSLAdapter(
            config.serverCertPem, config.serverCertKey)
        try:
            server.start()
        finally:
            server.stop()

# Create the default bottle app and then wrap it around
# a beaker middleware and send it back to bottle to run
run(app=default_app(), host='0.0.0.0', port=443, server=SSLCherryPyServer)
'''
###############################################################################


# run(host=config.host, port=config.server_port, reloader=config.auto_reload)








"""
Inicio normal:
nohup python3 /home/cls/pyTunes/jsonApiServer/index.py &

Mater logs de requests http:
nohup python3 /home/cls/pyTunes/jsonApiServer/index.py
>> /home/cls/pyTunes/jsonApiServer/log.txt

DEBUG com feedback para a linha de comandos:
python3 /home/cls/pyTunes/jsonApiServer/index.py

ps ax | grep /jsonApiServer/index.py
"""
