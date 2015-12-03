# coding=utf-8

import hashlib
from motorengine import fields

import settings
from libs.base_doc import BaseDoc


class User(BaseDoc):

    __collection__ = 'user'

    STATUS_LIST = ['ERROR', 'ACTIVE', 'DELETED']

    name = fields.StringField(db_field='name', max_length=50, unique=True,
                              required=True)
    password = fields.StringField(db_field='password', max_length=50,
                                  required=True)
    last_login = fields.DateTimeField(db_field='last_login', required=False)
    role_id = fields.StringField(db_field='role_id', max_length=50,
                                 required=True)
    status = fields.StringField(db_field='status', max_length=20, required=True,
                                default="ACTIVE")

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


class Role(BaseDoc):

    __collection__ = 'role'

    STATUS_LIST = ['ERROR', 'ACTIVE', 'DELETED']
    key = fields.StringField(db_field='key', max_length=50, unique=True,
                             required=True)
    name = fields.StringField(db_field='name', max_length=50, required=True)
    status = fields.StringField(db_field='status', max_length=20, required=True,
                                default="ACTIVE")
