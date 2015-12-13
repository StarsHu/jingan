# -*- coding: utf-8 -*-

from tornado.web import authenticated
from tornado.gen import coroutine

from models import Order, Yard
from libs.base_handler import BaseHandler


class OrderListHandler(BaseHandler):

    route_map = r'/order/list'

    @authenticated
    @coroutine
    def get(self):
        orders = yield Order.objects.filter(status='ACTIVE').find_all()
        self.render('order_list.html', orders=orders)


class OrderAddHandler(BaseHandler):

    route_map = r'/order/add'

    @authenticated
    @coroutine
    def get(self):
        yards = yield Yard.objects.find_all()
        self.render('order_add.html', yards=yards)
