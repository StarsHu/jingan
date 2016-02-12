# -*- coding: utf-8 -*-

import json
import settings
import logging
from tornado.web import RequestHandler
from tornado.web import URLSpec

from libs.json_encoder import ComplexEncoder

def authorized(func):

    def __wrapper(*args, **kwargs):
        import pdb; pdb.set_trace()
        return func(*args, **kwargs)

    return __wrapper


class BaseHandler(RequestHandler):

    route_map = None
    route_kwargs = None
    route_name = None

    context = dict()
    query = ''
    page = settings.default_active_page
    count_per_page = settings.default_count_per_page

    logger = logging.getLogger("tornado.application")

    errors = list()

    SOURCE_LIST_DISPLAY = {
        'JINGDO': '京东',
        'TMALL': '天猫',
        'SUNING': '苏宁',
        'YIHAODIAN': '一号店',
        'FEINIU': '飞牛',
    }

    @classmethod
    def get_url_spec(cls):
        return URLSpec(cls.route_map, cls, cls.route_kwargs, cls.route_name)

    @classmethod
    def to_son(cls, obj):
        return json.dumps(obj, cls=ComplexEncoder)

    @classmethod
    def from_son(cls, string):
        return json.loads(string)

    def get_current_user(self):
        auth_cookie = self.get_secure_cookie(settings.auth_cookie_name, None)
        if auth_cookie:
            try:
                self.current_user = self.from_son(str(auth_cookie, 'utf-8'))
                return self.current_user
            except Exception as e:
                self.logger.info(e)
        return None

    def prepare(self):
        try:
            self.query = self.get_argument('q')
            self.context['q'] = self.query
        except:
            pass
        try:
            self.page = int(self.get_argument('p'))
            if self.page < 1:
                raise
            self.context['p'] = self.page
        except:
            pass

    def write_son(self, obj, status_code=200):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self._status_code = status_code
        return self.write(self.to_son(obj))
