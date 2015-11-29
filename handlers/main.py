# coding=utf-8

from tornado.web import URLSpec

from __init__ import urls
from lib.base_handler import BaseHandler


class HomeHandler(BaseHandler):

    def get(self):
        self.write("Hello, world")

urls += URLSpec('/', HomeHandler)
