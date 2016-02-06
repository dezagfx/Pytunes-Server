from sqlalchemy import (Table, Column, Integer, String, MetaData,
                        Sequence)
from ._connection import connection
from ._base_model import BaseModel


m = MetaData()


class User(BaseModel):

    table = Table(
        'users',
        MetaData(),
        Column('id', Integer, Sequence('user_id_seq'), primary_key=True),
        Column('name', String(255)),
        Column('email', String(255)),
        Column('password', String(255)),
        Column('salt', String(255))
    )

    def __init__(self, name, email, password, salt):
        self.name = name
        self.email = email
        self.password = password
        self.salt = salt

    def save(self):
        s = self.table.insert().values(
                name=self.name,
                email=self.email,
                password=self.password,
                salt=self.salt
            )
        connection.execute(s)

    @staticmethod
    def get_by_name(name):
        s = User.table.select().where(User.table.c.name == name)
        return connection.execute(s).fetchone()

    @staticmethod
    def get_by_email(email):
        s = User.table.select().where(User.table.c.email == email)
        return connection.execute(s).fetchone()
