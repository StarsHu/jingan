# coding=utf-8

from tornado.web import RequestHandler
from tornado.web import URLSpec


class BaseHandler(RequestHandler):

    route_map = None
    route_kwargs = None
    route_name = None

    @classmethod
    def get_url_spec(cls):
        return URLSpec(cls.route_map, cls, cls.route_kwargs, cls.route_name)
