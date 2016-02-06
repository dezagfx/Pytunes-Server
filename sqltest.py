# from config import config
# from models import *
from sqlalchemy import (Table, Column, Integer, String, Boolean, MetaData,
    ForeignKey, Sequence, func,create_engine)
from sqlalchemy.sql import select
metadata = MetaData()

users_table = Table(
    'users',
    metadata,
    Column('id', Integer, Sequence('user_id_seq'), primary_key=True),
    Column('name', String(255)),
    Column('password', String(255)),
    Column('salt', String(255)),
)

playlists_table = Table(
    'playlists',
    metadata,
    Column('id', Integer, Sequence('user_id_seq'), primary_key=True),
    Column('name', String(255)),
    Column('user_id', None, ForeignKey('users.id')),
    Column('is_private', Boolean())
)


db_user = 'pytunes'
db_name = 'pytunes'
db_host = '178.79.165.224'
db_pass = 'Lmxy20#a'
db_port = '3306'

connection_string = 'mysql+pymysql://' + db_user+':'+db_pass+'@'+db_host+'/'+db_name
engine = create_engine(connection_string, echo=False)
db_connection = engine.connect()
'''
# s = select([func.count(users_table.c.id)]).where(users_table.c.name == 'ruben')
# print(s)
# s = select([users_table]).where(users_table.c.name == 'rui')
s = select([func.count(users_table.c.id)]).\
    where(users_table.c.name == 'ruben')
users_result = db_connection.execute(s).fetchall()
# print(len(users_result))
print(users_result[0][0])
'''

name = 'ruben'

s = select([users_table.c.id, users_table.c.password, users_table.c.salt]). \
    where(users_table.c.name == name)
users_result = db_connection.execute(s).fetchall()


print(len(users_result))
print(users_result[0]['id'])

for user in users_result:
    print('NOME:', user['id'])


print('FIM')
'''
s = select([playlists_table])
pl_result = db_connection.execute(s)
for pl in pl_result:
    print('NOME:',pl['name'])
'''