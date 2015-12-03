#!/usr/bin/env python3
# coding=utf8

import inspect
import importlib
from tornado.web import Application

import settings
from libs.base_handler import BaseHandler
from libs.jinja import JinjaLoader


def get_handler_from_module(module):
    handlers = []
    if inspect.ismodule(module) and hasattr(module, '__all__'):
        for sub_module_name in module.__all__:
            sub_module_path = '.'.join([module.__name__, sub_module_name])
            sub_module = importlib.import_module(sub_module_path)
            handlers += get_handler_from_module(sub_module)
    else:
        attrs = dir(module)
        for attr_name in attrs:
            if not attr_name.startswith('_'):
                attr = module.__dict__[attr_name]
                if inspect.isclass(attr) \
                        and issubclass(attr, BaseHandler) \
                        and attr.route_map:
                    handlers.append(attr.get_url_spec())
    return handlers


app_handlers = []
for package_name in settings.handler_packages:
    package = importlib.import_module(package_name)
    app_handlers += get_handler_from_module(package)
app_handlers = list(set(app_handlers))

app_settings = {
    'debug': settings.debug,
    'auto_reload': True,
    'compress_response': True,
    'servce_traceback': True,
    'cookie_secret': settings.cookie_secret,
    'xsrf_cookies': True,
    'static_path': settings.static_root,
    'static_url_prefix': settings.static_url,
    'login_url': settings.auth_login_url,
    'template_loader': JinjaLoader(settings.template_root),
}

app = Application(app_handlers, **app_settings)
