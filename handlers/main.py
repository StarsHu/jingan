# coding=utf-8

from tornado.web import authenticated

from libs.base_handler import BaseHandler


class HomeHandler(BaseHandler):

    route_map = r'/'

    @authenticated
    def get(self):
        self.render('home.html')
