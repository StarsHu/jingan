# -*- coding: utf-8 -*-

import settings
from bson import BSON
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
        auth_cookie = self.get_secure_cookie(settings.auth_cookie_name, None)
        if auth_cookie:
            try:
                self.current_user = BSON.decode(auth_cookie)
                return self.current_user
            except:
                pass
        return None

    def prepare(self):
        pass
