# /usr/bin/env python
# from bottle import route, run, template, request
from bottle import (route, response, run, redirect, request, static_file,
                    ServerAdapter, default_app, template, )
import json
from config import config


@route('/')
def test():
    userName = request.query.userName
    if userName == 'ruben':
        return template('{{!name}}', name=userName)
    return 'erro'


@route('/admin/list-users')
def index():
    return '<b>Hello </b>!' + str(config.debugMode)


@route('/playlist/<id>')
def singlePlaylist(id):
    struct = {
                    1: {'name': 'Yellow Submarine', 'artist': 'The Beattles'}
                }
    return json.dumps(struct)


@route('/auth/login', method='POST')
def authenticate():
    userName = request.forms.get('userName')
    password = request.forms.get('password')
    if userName == 'ruben':
        return template('<b>{{!name}} </b>', name=userName)
    return 'erro'


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

###############################################################################
run(host=config.host, port=config.serverPort, reloader=config.autoReload)


"""
Inicio normal:
nohup python3 /home/cls/pyTunes/jsonApiServer/index.py &

Mater logs de requests http:
nohup python3 /home/cls/pyTunes/jsonApiServer/index.py & >> /home/cls/pyTunes/jsonApiServer/log.txt

DEBUG com feedback para a linha de comandos:
python3 /home/cls/pyTunes/jsonApiServer/index.py

ps ax | grep /jsonApiServer/index.py
"""
