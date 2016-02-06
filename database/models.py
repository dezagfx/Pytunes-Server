from sqlalchemy import (Table, Column, Integer, String, MetaData, ForeignKey,
                        Sequence)
from .connection import connection
##
from sqlalchemy.orm import Query
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

metadata = MetaData()

'''
class BaseModel(object):
    @staticmethod
    def validate():
        print('validate')

    def get_table_fields_names(self):
        for c in self.table.c:
            print(c)

    def test(self):
        import inspect
        print(inspect.getfile(self.table.__class__))
'''


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
        Column('file', String(255)),
        Column('owner_id',  None, ForeignKey('users.id')),
    )

    def __init__(self, name, file, owner_id):
        self.name = name
        self.file = file
        self.owner_id = owner_id

    def save(self):
        s = self.table.insert().values(
                name=self.name,
                file=self.file,
                owner_id=self.owner_id,
            )
        connection.execute(s)

    @staticmethod
    def get_all_public_musics():
        return None

    @staticmethod
    def get_all_by_user_id(user_id):
        s = Music.table.select().where(Music.table.c.user_id == user_id)
        return connection.execute(s).fetchall()


class Playlist():

    table = Table(
        'playlists',
        metadata,
        Column('id', Integer, Sequence('playlist_id_seq'), primary_key=True),
        Column('name', String(255)),
        Column('user_id', None, ForeignKey('users.id')),
    )

    def __init__(self, name, file, user_id):
        self.name = name
        self.file = file
        self.user_id = user_id

    def save(self):
        s = self.table.insert().values(
                name=self.name,
                file=self.file,
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
