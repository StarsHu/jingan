#!/usr/bin/env python3
# coding=utf8

import os
import inspect
import importlib
from tornado.web import Application
from tornado.web import URLSpec

import settings
from lib.base_handler import BaseHandler

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
                if issubclass(attr, BaseHandler) and attr.route_map:
                    handlers.append(attr.get_url_spec())
    return handlers


handlers = []
#handlers.append(main.HomeHandler.get_url_spec())
for package_name in settings.handler_packages:
    package = importlib.import_module(package_name)
    handlers += get_handler_from_module(package)

app = Application(handlers)
