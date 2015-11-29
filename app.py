#!/usr/bin/env python3
# coding=utf8

import os
import importlib
from tornado.web import Application
from tornado.web import URLSpec

import settings
from lib.base_handler import BaseHandler


handlers = []
for package_name in settings.handler_packages:
    package = importlib.import_module(package_name)
    if hasattr(package, 'urls'):
        handlers += package.urls

app = Application(handlers)
