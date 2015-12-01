# coding=utf-8

import os

debug = True

port = 8000

# Please define your database config in my_conf.py
# database = {
#     'name': 'jingan',
#     'user': 'postgres',
#     'password': '123456',
#     'host': '127.0.0.1',
# }

handler_packages = [
    'libs.auth',
    'handlers',
]

project_root = os.path.dirname(os.path.abspath(__file__))

auth_login_url = '/auth/login'

static_root = os.path.join(project_root, 'static')
static_url = '/static/'

cookie_secret = "56f11205eceb0d197e457eb75f9a42b5"

from my_conf import *
