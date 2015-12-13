# -*- coding: utf-8 -*-

from tornado.web import authenticated
from tornado.gen import coroutine

from models import User
from libs.base_handler import BaseHandler


class UserListHandler(BaseHandler):

    route_map = r'/user/list'

    @authenticated
    @coroutine
    def get(self):
        users = yield User.objects.filter(status='ACTIVE').find_all()
        self.render('user_list.html', users=users)
