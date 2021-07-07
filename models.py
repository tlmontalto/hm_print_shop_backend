import os
from datetime import datetime

from peewee import *
from flask_login import UserMixin
from playhouse.db_url import connect

# import boto3
# s3 = boto3.resource('s')

if 'ON_HEROKU' in os.environ:
    DATABASE = PostgresqlDatabase('dfgaaipjmoouah', user='yomnzeafsjhioq', password='91137a853bf3868ac2990020b452c5b5146fd29deac3ac800b85d6d8ecc06100', host='ec2-54-147-93-73.compute-1.amazonaws.com', port=5432)
else:
    DATABASE = PostgresqlDatabase('hmprintshop')

class HMPUser(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()
    created_at = DateTimeField(default = datetime.now)

    class Meta:
        database = DATABASE

class Link (Model):
    username = CharField()
    description = CharField()
    file_url = CharField()
    created_at = DateTimeField(default = datetime.now)

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([HMPUser, Link], safe=True)
    print('Peewee connected and tables created')
    DATABASE.close()