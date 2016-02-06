# Qual o caminho base ?
import os
_config_path = os.path.dirname(os.path.realpath(__file__))
# Andar um directorio para cima
base_path = '/'.join(_config_path.split('/')[0:-1])

# Se devemos ou nao reiniciar o processo a cada request
# adiciona alguma latencia mas e util para desenvolvimento
# bool
auto_reload = True

# Porta na qual o servidor escuta
# int
server_port = 8080

# 0.0.0.0 escuta em todos os interfaces de rede
# str
host = '0.0.0.0'

# apache | SSLWSGIRefServer
server_type = 'SSLWSGIRefServer'


###############################################################################
# Caminhos dos certificados SSL:
###############################################################################
serverCertPem = base_path + '/ssl_certs/pyTunes.pem'
serverCertKey = base_path + '/ssl_certs/pyTunes.key'
