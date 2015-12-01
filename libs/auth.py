# coding=utf-8

import peewee_async
from tornado.gen import coroutine

import settings
from models import User
from libs.base_handler import BaseHandler


class AuthHandler(BaseHandler):

    route_map = settings.auth_login_url

    @coroutine
    def get(self, *args, **kwargs):
        user = yield from peewee_async.get_object(
            User,
            User.name == 'test',
            User.password == 'tt'
        )
        self.set_secure_cookie("user", 'cula')
        self.logger.info('cula login.')
        self.redirect(self.get_argument('next', '/'))
