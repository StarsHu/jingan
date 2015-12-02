# coding=utf-8

import json
import datetime
import peewee_async
from tornado.gen import coroutine
from tornado.web import authenticated

import settings
from models import User
from libs.base_handler import BaseHandler


class LoginHandler(BaseHandler):

    route_map = settings.auth_login_url

    def get(self):
        if self.get_current_user():
            return self.redirect(self.get_argument('next', '/'))
        else:
            return self.render('auth/login.html')

    @coroutine
    def post(self):
        try:
            user = yield from peewee_async.get_object(
                User, User.name == self.get_argument('username'))
        except User.DoesNotExist:
            return self.render('auth/login.html',
                               errors=["用户不存在."], username=user.name)
        if user.check_raw_password(self.get_argument('password')):
            expire_days = None
            if self.get_argument('remember_me', None):
                expire_days = 7
            user.last_login = datetime.datetime.now()
            user.update_at = datetime.datetime.now()
            yield from peewee_async.update_object(
                user, only=[User.last_login, User.update_at])
            self.set_secure_cookie(
                settings.auth_cookie_name,
                json.dumps({
                    'id': user.id,
                    'name': user.name,
                    'last_login': user.last_login
                }, default=datetime.datetime.isoformat),
                expire_days
            )
            self.logger.info('%s %s login.' % (user.id, user.name))
            return self.redirect(self.get_argument('next', '/'))
        else:
            return self.render('auth/login.html',
                               errors=["密码错误."], username=user.name)


class LogoutHandler(BaseHandler):

    route_map = settings.auth_logout_url

    @authenticated
    def get(self):
        self.clear_cookie(settings.auth_cookie_name)
        return self.redirect(self.get_argument('next', '/'))


class ChangePasswordHandler(BaseHandler):

    route_map = r'/auth/password/change'

    @authenticated
    def get(self):
        return self.render('auth/change_password.html')

    @authenticated
    @coroutine
    def post(self):
        try:
            user = yield from peewee_async.get_object(
                User, User.id == self.current_user['id'])
        except User.DoesNotExist:
            return self.render('auth/login.html',
                               errors=["这是一个不该遇到的错误,请告知管理员."])
        if user.check_raw_password(self.get_argument('old_password')):
            new_password = self.get_argument('new_password')
            new_password_again = self.get_argument('new_password_again')
            if (new_password != new_password_again):
                return self.render('auth/change_password.html',
                                errors=["两次密码输入不一致."])
            user.set_password(new_password_again)
            user.update_at = datetime.datetime.now()
            yield from peewee_async.update_object(
                user, only=[User.password, User.update_at])
            return self.redirect('/auth/logout')
        else:
            return self.render('auth/change_password.html',
                               errors=["旧密码错误."])
