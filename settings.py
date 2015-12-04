# coding=utf-8

import os
import pytz

debug = True

port = 8000

tz = pytz.UTC

# Please define your mongodb config in my_conf.py
database = {
    # 'name': 'your_db_name',
    'host': '127.0.0.1',
    'port': 27017
}

handler_packages = [
    'handlers',
]

project_root = os.path.dirname(os.path.abspath(__file__))

template_root = os.path.join(project_root, 'templates/')

auth_cookie_name = 'user'
auth_login_url = '/auth/login'
auth_logout_url = '/auth/logout'

static_root = os.path.join(project_root, 'static')
static_url = '/static/'

cookie_secret = "56f11205eceb0d197e457eb75f9a42b5"

try:
    import my_conf
    database.update(my_conf.database)
except:
    pass
