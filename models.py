from peewee import *
from flask_login import UserMixin

DATABASE = SqliteDatabase('disconnect.db')


class User(UserMixin, Model):
    uid = CharField(unique=True)
    username = CharField(unique=True, default='')
    temp_password = CharField(default='none')
    admin = BooleanField(default=False)

    class Meta:
        database = DATABASE
        order_by = ('-uid',)


class EditorPick(Model):
    """ Model for Editor's pick art & music content"""
    # 0 - art, 1 - music
    # Adding genres later

    cat = IntegerField()
    content = CharField()

    class Meta:
        database = DATABASE


def initialize():
        DATABASE.connect()
        DATABASE.create_tables([User, EditorPick], safe=True)
        DATABASE.close()
