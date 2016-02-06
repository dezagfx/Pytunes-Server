from sqlalchemy import (Table, Column, Integer, String, Boolean, MetaData,
                        ForeignKey, Sequence, func)
from .connection import connection

metadata = MetaData()

table = Table(
    'musics',
    metadata,
    Column('id', Integer, Sequence('session_id_seq'), primary_key=True),
    Column('name', String(255)),
    Column('file', String(255)),
    Column('owner_id',  None, ForeignKey('users.id')),
    Column('is_private', Boolean())

)


def get_all_public_musics():
    return None


def get_all_musics_by_user_id(id):
    return None
