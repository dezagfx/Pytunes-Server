from sqlalchemy import (Table, Column, Integer, String, MetaData, ForeignKey,
                        Sequence)
from database._connection import connection

metadata = MetaData()

sessions = Table(
    'sessions',
    metadata,
    Column('id', Integer, Sequence('session_id_seq'), primary_key=True),
    Column('user_id',  Integer, ForeignKey('users.id')),
    Column('token', String(255)),
)


def delete_session(token):
    s = sessions.delete().where(sessions.c.token == token)
    result = connection.execute(s)
    if result.rowcount == 1:
        return True
    return False


def token_exists(token):
    s = sessions.select().where(sessions.c.token == token)
    if connection.execute(s).fetchone() != None:
        return True
    return False


def get_user_id_by_token(token):
    # Assumimos que o user_id tem de estar SEMPRE definido
    s = sessions.select(sessions.c.user_id).where(sessions.c.token == token)
    result = connection.execute(s).fetchone()
    return result.user_id
