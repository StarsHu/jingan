# coding=utf-8

import peewee_async
from tornado.gen import coroutine

import settings
from models import User
from libs.base_handler import BaseHandler


class AuthHandler(BaseHandler):

    route_map = settings.auth_login_url

    def get(self):
        return self.render('login.html')

    @coroutine
    def post(self, *args, **kwargs):
        try:
            user = yield from peewee_async.get_object(
                User, User.name == self.get_argument('username'))
        except User.DoesNotExist:
            return self.render('login.html',
                               errors=["用户不存在."], username=user.name)
        if user.check_raw_password(self.get_argument('password')):
            expire_days = None
            if self.get_argument('remember_me', None):
                expire_days = 7
            self.set_secure_cookie("user", str(user.id), expire_days)
            self.logger.info('%s %s login.' % (user.id, user.name))
            self.redirect(self.get_argument('next', '/'))
        else:
            return self.render('login.html',
                               errors=["密码错误."], username=user.name)
