#!/usr/bin/env python3
# coding=utf8

import logging
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import parse_command_line

import settings
from app import app

http_server = HTTPServer(app, xheaders=True)
http_server.listen(settings.port)

if __name__ == "__main__":
    logger = logging.getLogger("tornado.application")
    parse_command_line()
    logger.info('Server running on http://0.0.0.0:%d' % (settings.port))
    IOLoop.instance().start()
