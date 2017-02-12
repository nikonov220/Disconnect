from peewee import *
from flask_login import UserMixin

DATABASE = SqliteDatabase('disconnect.db')


class User(UserMixin, Model):
    uid = CharField(unique=True)
    username = CharField(unique=True, default='')
    temp_password = CharField(default='none')

    class Meta:
        database = DATABASE
        order_by = ('-uid',)


def initialize():
        DATABASE.connect()
        DATABASE.create_tables([User], safe=True)
        DATABASE.close()
