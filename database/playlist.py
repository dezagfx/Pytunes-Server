from sqlalchemy import (Table, Column, Integer, String, Boolean, MetaData,
                        ForeignKey, Sequence, func)
from database._connection import connection

metadata = MetaData()

playlists = Table(
    'playlists',
    metadata,
    Column('id', Integer, Sequence('playlist_id_seq'), primary_key=True),
    Column('name', String(255)),
    Column('user_id', None, ForeignKey('users.id')),
    Column('is_private', Boolean())
)


def create(name, user_id, is_private=0):
    return


def get_all_playlists_by_user_id(id):
    return None
