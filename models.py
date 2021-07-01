from datetime import datetime

from peewee import *
from flask_login import UserMixin


DATABASE = PostgresqlDatabase('hmprintshop')

class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()
    created_at = DateTimeField(default = datetime.now)

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User], safe=True)
    print('Peewee connected and tables created')
    DATABASE.close()