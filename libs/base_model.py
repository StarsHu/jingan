# coding=utf-8

import datetime
import peewee

import settings


class BaseModel(peewee.Model):

    create_at = peewee.DateTimeField(default=datetime.datetime.now)
    update_at = peewee.DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        self.update_at = datetime.datetime.now()
        super(BaseModel, self).save(*args, **kwargs)
