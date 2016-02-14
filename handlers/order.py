# coding=utf-8

import datetime
from tornado.web import authenticated
from tornado.gen import coroutine
from bson.objectid import ObjectId
from models import Order, Yard, Product
from motorengine.query_builder.node import Q
from motorengine import DESCENDING
from libs.base_handler import BaseHandler, authorized
from libs.form_error import FormError


class OrderPageListHandler(BaseHandler):

    route_map = r'/order/list'

    @authenticated
    @authorized(['salesmanager', 'admin'])
    @coroutine
    def get(self):
        query = Q(status='ACTIVE')
        if self.query:
            q = '.*%s.*' % self.query
            query = query & (
                Q({"seller": {'$regex': q}})
            )
        qs = Order.objects.filter(query).order_by('deliver_at',
                                                  direction=DESCENDING)
        total = yield qs.count()
        if self.page:
            skip = self.count_per_page * (self.page - 1)
            limit = self.count_per_page
            qs = qs.skip(skip).limit(limit)
        orders = yield qs.find_all()
        yards = yield Yard.objects.find_all()
        products = yield Product.objects.find_all()
        self.context['total'] = total / self.count_per_page
        self.context['orders'] = orders
        self.context['yards'] = yards
        self.context['products'] = products
        self.render('order_list.html', **self.context)


class OrderCreateHandler(BaseHandler):

    route_map = r'/order/create'

    @authenticated
    @authorized(['salesmanager', 'admin'])
    @coroutine
    def post(self):
        source = self.get_argument('source')
        seller = self.get_argument('seller')
        yard_id = self.get_argument('yard_id')
        deliver_at = datetime.datetime.strptime(
            self.get_argument('deliver_at'), "%Y-%m-%d")

        yard = yield Yard.objects.get(ObjectId(yard_id))

        order = Order(
            source=source,
            seller=seller,
            yard=yard,
            deliver_at=deliver_at
        )
        yield order.save()

        return self.write_son({
            'redirect': '/order/list',
        })


class OrderUpdateHandler(BaseHandler):

    route_map = r'/order/update/(.*)'

    @authenticated
    @authorized(['salesmanager', 'admin'])
    @coroutine
    def post(self, id):
        source = self.get_argument('source', None)
        region = self.get_argument('region', None)
        name = self.get_argument('name', None)
        phone = self.get_argument('phone', None)
        address = self.get_argument('address', None)

        order = yield Order.objects.get(ObjectId(id))
        if source is not None:
            order.source = source
        if region is not None:
            order.region = region
        if name is not None:
            order.name = name
        if phone is not None:
            order.phone = phone
        if address is not None:
            order.address = address

        yield order.save()
        return self.write_son({})


class OrderDeleteHandler(BaseHandler):

    route_map = r'/order/delete/(.*)'

    @authenticated
    @authorized(['salesmanager', 'admin'])
    @coroutine
    def post(self, id):
        order = yield Order.objects.get(ObjectId(id))
        yield order.delete()
        return self.write_son({})
