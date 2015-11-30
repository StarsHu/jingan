# coding=utf-8

import logging
from tornado.web import RequestHandler
from tornado.web import URLSpec


class BaseHandler(RequestHandler):

    route_map = None
    route_kwargs = None
    route_name = None

    logger = logging.getLogger("tornado.application")

    @classmethod
    def get_url_spec(cls):
        return URLSpec(cls.route_map, cls, cls.route_kwargs, cls.route_name)

    def get_current_user(self):
        user = self.get_secure_cookie("user")
        return user

    def prepare(self):
        pass
