# coding=utf-8

import datetime

import peewee


class BaseModel(peewee.Model):

    create_time = peewee.DateTimeField(default=datetime.datetime.now)
    update_time = peewee.DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        self.update_time = datetime.datetime.now()
        super(BaseModel, self).save(*args, **kwargs)
