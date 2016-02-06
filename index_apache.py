# /usr/bin/env python
import bottle
from bottle import (route, response, run, redirect, request, static_file,
                    ServerAdapter, default_app, template, error, hook, abort)
import json
from config import config
from models import *
###############################################################################
# Qual o caminho base ?
# To-do: Tentar mudar isto para dentro do ficheiro config.py
import os
global base_path
base_path = os.path.dirname(os.path.realpath(__file__))

# Adicionar o caminho completo para a localizaçao das views
bottle.TEMPLATE_PATH.insert(0, base_path + '/views/')
###############################################################################


@hook('before_request')
def before_request():
    # print(bottle.default_app().routes)
    # bottle.py linha 612
    for r in bottle.default_app().routes:
        print(r.rule)
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
        from services import auth_service as auth
        if not auth.is_authenticated(request):
            # abort(): bottle.py linha 2457
            # Levanta uma excepç~ao HTTPError definida em bottle.py linha 1811
            abort(403, auth.auth_error)
    '''

    # Antes do pedido chegar ao router da framwork interceptamos o pedido e
    # verificamos qual o HTTP_USER_AGENT presente no header do pedido.
    # Criamos uma variavel global que identifica qual o tipo de cliente
    # que sera posteriormente utilizada para decidir se utilizamos cookies na
    # autenticacao ou passamos o valor da id de sessao atraves de json para o
    # cliente

    user_agent = request.environ.get('HTTP_USER_AGENT')
    global api_client
    api_client = 'pyTunes' if user_agent == 'pyTunes' else 'browser'

    # O parametro 'Host' do header pode ser manipulado e, regra geral, nao e
    # boa ideia confiar, mas aqui vamos usa-lo de forma a podermos detectar
    # dinamicamente o ip

    # Qual o ip base / url base? Em vez de termos este valor 'hard coded'
    # detectamo-lo para cada pedido (permite alternar entre ip's facilmente):
    global http_host
    http_host = bottle.request.get_header('host')
    global base_url
    base_url = 'https://' + http_host + '/'
    global assets_base_url
    assets_base_url = base_url + 'assets/'

###############################################################################


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
    return static_file(filepath, root=base_path+'/assets')


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
    # template('I live at {{number}} {{street}}, {{city}}', **view_data)
    return template('docs/index', **view_data)


@route('/docs', method='GET')
def docs():
    view_data = {
        'base_url': base_url,
        'assets_base_url': assets_base_url
    }
    # template('I live at {{number}} {{street}}, {{city}}', **view_data)
    return template('docs/index', **view_data)


@route('/playlist/<id>')
def singlePlaylist(id):
    message = [
                {'name': 'Musica 1', 'artist': 'Artista 1'},
                {'name': 'Musica 2', 'artist': 'Artista 2'},
                {'name': 'Musica 3', 'artist': 'Artista 3'},
                {'name': 'Musica 4', 'artist': 'Artista 4'},
                {'name': 'Musica 5', 'artist': 'Artista 5'},
                {'name': 'Musica 6', 'artist': 'Artista 6'},
                {'name': 'Musica 7', 'artist': 'Artista 7'},
                {'name': 'Musica 8', 'artist': 'Artista 8'},
                {'name': 'Musica 9', 'artist': 'Artista 9'},
                {'name': 'Musica 1', 'artist': 'Artista 1'},
                {'name': 'Musica 2', 'artist': 'Artista 2'},
                {'name': 'Musica 3', 'artist': 'Artista 3'},
                {'name': 'Musica 4', 'artist': 'Artista 4'},
                {'name': 'Musica 5', 'artist': 'Artista 5'},
                {'name': 'Musica 6', 'artist': 'Artista 6'},
                {'name': 'Musica 7', 'artist': 'Artista 7'},
                {'name': 'Musica 8', 'artist': 'Artista 8'},
                {'name': 'Musica 9', 'artist': 'Artista 9'},
                {'name': 'Musica 1', 'artist': 'Artista 1'},
                {'name': 'Musica 2', 'artist': 'Artista 2'},
                {'name': 'Musica 3', 'artist': 'Artista 3'},
                {'name': 'Musica 4', 'artist': 'Artista 4'},
                {'name': 'Musica 5', 'artist': 'Artista 5'},
                {'name': 'Musica 6', 'artist': 'Artista 6'},
                {'name': 'Musica 7', 'artist': 'Artista 7'},
                {'name': 'Musica 8', 'artist': 'Artista 8'},
                {'name': 'Musica 9', 'artist': 'Artista 9'},
            ]
    response.set_header('Content-Type', 'application/json; charset=UTF-8')
    return json.dumps(message)


###############################################################################
# Autenticaç~ao
###############################################################################


@route('/auth/login', method='POST')
def auth_login():
    user_name = request.forms.get('user_name')
    password = request.forms.get('password')
    if user_name == 'ruben' and password == '123':
        message = {
                        'success': True,
                        'token': 'TOKEN1234'
                    }
        return json.dumps(message)
        # return template('<b>{{!name}} </b>', name=userName)
    return 'erro'


@route('/auth/logout', method='POST')
def auth_logout():
    user_name = request.forms.get('user_name')
    password = request.forms.get('password')
    if user_name == 'ruben' and password == '123':
        message = {
                        'success': True,
                        'serssion_token': 'TOKEN1234'
                    }
        return json.dumps(message)
        # return template('<b>{{!name}} </b>', name=userName)
    return 'erro'


@route('/auth/check', method='POST')
def auth_check():
    userName = request.forms.get('userName')
    # password = request.forms.get('password')
    if userName == 'ruben' and password:
        return template('<b>{{!name}} </b>', name=userName)
    return 'erro'


















@route('/admin/users')
def admin_listUsers():
    return '<b>Hello </b>!' + str(config.debugMode)


###############################################################################
# http://www.socouldanyone.com/2014/01/bottle-with-ssl.html
class SSLWSGIRefServer(ServerAdapter):
    def run(self, handler):
        from wsgiref.simple_server import make_server, WSGIRequestHandler
        import ssl
        if self.quiet:
            class QuietHandler(WSGIRequestHandler):
                def log_request(*args, **kw): pass
            self.options['handler_class'] = QuietHandler
        srv = make_server(self.host, self.port, handler, **self.options)
        srv.socket = ssl.wrap_socket(
            srv.socket,
            certfile=config.serverCertPem,  # caminho para o certificado
            keyfile=config.serverCertKey,  # caminho para o certificado
            server_side=True)
        srv.serve_forever()

###############################################################################
"""
Daqui inicializamos o servidor que herda do ServerAdapter da framwork bottle
passando para o construtor (bottle.py linha 2782) o host e a porta
"""
srv = SSLWSGIRefServer(
        host=config.host,
        port=config.serverPort,
    )

run(server=srv, reloader=config.autoReload)

# run(host=config.host, port=config.serverPort, reloader=config.autoReload)


"""
Inicio normal:
nohup python3 /home/cls/pyTunes/jsonApiServer/index.py &

Mater logs de requests http:
nohup python3 /home/cls/pyTunes/jsonApiServer/index.py & 
>> /home/cls/pyTunes/jsonApiServer/log.txt

DEBUG com feedback para a linha de comandos:
python3 /home/cls/pyTunes/jsonApiServer/index.py

ps ax | grep /jsonApiServer/index.py
"""
