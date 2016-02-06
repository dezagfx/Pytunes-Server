import json
from config import config
# from database.models import User
from services import json_response as jresp, auth
from sqlalchemy import (Table, Column, Integer, String, MetaData, ForeignKey,
                        Sequence)
# from .connection import connection

# metadata = MetaData()
# user.get_user_by_name('ruben')
# print(user.get_user_by_name('ruben2'))
# print(dir())

# print(session.get_user_id_by_token('AAA'))


# print(auth.hash_password('1234'))

# print(get_user_by_name('carlos'))
#u = User(name='a', email='a', password='a', salt='a')
#u.save()
# print(u.get_by_name('carlos'))
#u.test()

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Query, sessionmaker
from sqlalchemy import create_engine
from database import config

connection_string = str(
                'mysql+pymysql://' + config.db_user + ':' +
                config.db_pass + '@' + config.db_host + '/' +
                config.db_name
                    )
engine = create_engine(connection_string, echo=False)
connection = engine.connect()

Base = declarative_base()
Session = sessionmaker(bind=engine)


class BaseModel(object):

    errors = ['test']

    def validate():
        print('validate')

    def get_table_fields_names(self):
        for c in self.table.c:
            print(c)

    def test(self):
        import inspect
        print(inspect.getfile(self.table.__class__))


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column('name', String(255), nullable=False)
    email = Column('email', String(255), nullable=False)
    password = Column('password', String(255), nullable=False)

    def get_one_by_name(self):
        return


class Music(Base):

    __tablename__ = 'musics'

    id = Column(Integer, Sequence('music_id_seq'), primary_key=True)
    name = Column(String(255), nullable=False)
    file_name = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id
        self.file_name = '12345678976'

    def generate():
        return

###############################################################################
'''
session = Session()
user = User(name='2', _email='2', password='edspassword')
session.add(user)
# session.commit()
print(user.id)
'''
'''
session = Session()
music = Music(name='This Time', user_id=user.id)
session.add(music)
session.commit()
'''

