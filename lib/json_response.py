import json
from bottle import response


def reply(payload, success=True, error_message=None, status=200):

    client_response = {
        'success': True,
        'payload': {}
    }

    # http://stackoverflow.com/questions/12806386/
    # standard-json-api-response-format
    # ^ Apenas um guia base para servir de referencia
    if not success:
        client_response['success'] = False
        client_response.pop("payload", None)
        client_response['error_message'] = error_message
    else:
        client_response['payload'] = payload

    response.set_header('Content-Type', 'application/json; charset=UTF-8')
    response.status = status
    return json.dumps(client_response)
