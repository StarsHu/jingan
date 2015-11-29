#!/usr/bin/env python3
# coding=utf8

import time
import signal
import logging
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

import settings
from app import app

http_server = HTTPServer(app, xheaders=True)
http_server.listen(settings.port)

if __name__ == "__main__":
    logging.info('Server running on http://0.0.0.0:%d' % (settings.port))
    IOLoop.instance().start()
