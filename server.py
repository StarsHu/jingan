#!/usr/bin/env python3
# coding=utf8

import logging
import asyncio
from tornado.httpserver import HTTPServer
from tornado.options import parse_command_line
from tornado.platform.asyncio import AsyncIOMainLoop

import settings

AsyncIOMainLoop().install()

from app import app

http_server = HTTPServer(app, xheaders=True)
http_server.listen(settings.port)

# init database in debug
if settings.debug:
    from init_site import init_db
    init_db()

loop = asyncio.get_event_loop()
loop.run_until_complete(app.db.connect_async())

if __name__ == "__main__":
    logger = logging.getLogger("tornado.application")
    parse_command_line()
    logger.info('Server running on http://0.0.0.0:%d' % (settings.port))
    loop.run_forever()
