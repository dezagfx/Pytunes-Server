import os
import base64
import time
import bcrypt

auth_error = {
                'success': False,
                'message': 'Nao esta autorizado.'
            }


def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def password_matches(password, hashed):
    if bcrypt.hashpw(password.encode('utf-8'),
                     hashed.encode('utf-8')) == hashed.encode('utf-8'):
        return True
    return False


def generate_session_token():
    return base64.b64encode(os.urandom(32)).decode('utf-8') + str(time.time())

if __name__ == '__main__':
    print(hash_password('12234'))