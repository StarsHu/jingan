# coding=utf-8

import datetime
import peewee_async
from tornado.gen import coroutine

import settings
from models import User
from libs.base_handler import BaseHandler


class LoginHandler(BaseHandler):

    route_map = settings.auth_login_url

    def get(self):
        if self.get_current_user():
            return self.redirect(self.get_argument('next', '/'))
        else:
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
            user.last_login = datetime.datetime.now()
            user.update_at = datetime.datetime.now()
            yield from peewee_async.update_object(
                user, only=[User.last_login, User.update_at])
            self.set_secure_cookie("user", str(user.id), expire_days)
            self.logger.info('%s %s login.' % (user.id, user.name))
            return self.redirect(self.get_argument('next', '/'))
        else:
            return self.render('login.html',
                               errors=["密码错误."], username=user.name)


class LogoutHandler(BaseHandler):

    route_map = settings.auth_logout_url

    def get(self):
        self.clear_cookie('user')
        return self.redirect(self.get_argument('next', '/'))


