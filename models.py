# coding=utf-8

import asyncio
import peewee
import peewee_async

import settings

database = peewee_async.PostgresqlDatabase(
    settings.database['name'],
    user=settings.database['user'],
    password=settings.database['password'],
    host=settings.database['host']
)
loop = asyncio.get_event_loop()


class User(peewee.Model):
    name = peewee.CharField()

    class Meta:
        database = database

User.create_table(True)
database.close()
