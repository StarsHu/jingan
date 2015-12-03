#!/usr/bin/env python3
# coding=utf8

import logging
from tornado.httpserver import HTTPServer
from tornado.options import parse_command_line
from tornado.ioloop import IOLoop
from motorengine.connection import connect

import settings


from app import app

http_server = HTTPServer(app, xheaders=True)
http_server.listen(settings.port)

io_loop = IOLoop.current()
connect(
    settings.database['name'],
    host=settings.database['host'],
    port=settings.database['port'],
    io_loop=io_loop
)
# init database in debug
if settings.debug:
    from init_site import init_db
    io_loop.add_timeout(5, init_db)

if __name__ == "__main__":
    logger = logging.getLogger("tornado.application")
    parse_command_line()
    logger.info('Server running on http://0.0.0.0:%d' % (settings.port))
    io_loop.start()
