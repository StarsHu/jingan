# coding=utf-8

from lib.base_handler import BaseHandler


class HomeHandler(BaseHandler):

    route_map = '/'

    def get(self):
        self.write("Hello, world")
