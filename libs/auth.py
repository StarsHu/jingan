# coding=utf-8

from libs.base_handler import BaseHandler

import settings


class AuthHandler(BaseHandler):

    route_map = settings.auth_login_url

    def get(self, *args, **kwargs):
        self.set_secure_cookie("user", 'cula')
        self.logger.info('cula login.')
        self.redirect(self.get_argument('next', '/'))
