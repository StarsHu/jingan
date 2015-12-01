# coding=utf-8

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

    class Meta:
        db_table = 'user'
        database = database


class Group(BaseModel):
    name = peewee.CharField(null=False)

    class Meta:
        db_table = 'group'
        database = database
