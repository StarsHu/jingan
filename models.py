# coding=utf-8

import hashlib
import asyncio
import peewee
import peewee_async

import settings
from libs.base_model import BaseModel

database = peewee_async.PostgresqlDatabase(
    settings.database['name'],
    user=settings.database['user'],
    password=settings.database['password'],
    host=settings.database['host']
)


class User(BaseModel):
    name = peewee.CharField(null=False)
    password = peewee.CharField(null=False)
    group_id = peewee.IntegerField(null=False)

    @classmethod
    def encode_raw_password(cls, password):
        m = hashlib.md5()
        m.update(password.encode('utf-8'))
        return m.hexdigest()

    def check_raw_password(self, password):
        return self.check_encoded_password(self.encode_raw_password(password))

    def check_encoded_password(self, password):
        if password == self.password:
            return True
        else:
            return False

    def set_password(self, password):
        self.password = self.encode_raw_password(password)

    class Meta:
        db_table = 'user'
        database = database


class Group(BaseModel):
    name = peewee.CharField(null=False)

    class Meta:
        db_table = 'group'
        database = database
