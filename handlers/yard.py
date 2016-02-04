# -*- coding: utf-8 -*-

from tornado.web import authenticated
from tornado.gen import coroutine
from bson.objectid import ObjectId

from models import Yard, Yard
from motorengine.query_builder.node import Q
from libs.base_handler import BaseHandler
from libs.form_error import FormError


class YardPageListHandler(BaseHandler):

    route_map = r'/yard/list'

    @authenticated
    @coroutine
    def get(self):
        context = dict()
        q = self.get_arguments("q")
        query = Q(status='ACTIVE')
        if len(q) > 0:
            context['q'] = q[0]
            q = '.*%s.*' % q[0]
            query = query & (
                Q({"name": {'$regex': q}})
                | Q({"region": {'$regex': q}})
                | Q({"phone": {'$regex': q}})
                | Q({"address": {'$regex': q}})
            )
        yards = yield Yard.objects.filter(query).find_all()
        context['yards'] = yards
        self.render('yard_list.html', **context)


class YardAddHandler(BaseHandler):

    route_map = r'/yard/add'

    @authenticated
    @coroutine
    def get(self):
        self.render('yard_add.html')

    @authenticated
    @coroutine
    def post(self):
        source = self.get_argument('source')
        region = self.get_argument('region')
        name = self.get_argument('name', '')
        phone = self.get_argument('phone', '')
        address = self.get_argument('address', '')

        yard = Yard(
            source=source,
            region=region,
            name=name,
            phone=phone,
            address=address,
        )
        yield yard.save()

        yards = yield Yard.objects.find_all()
        return self.write_son({
            'redirect': '/yard/list',
        })


class YardEditHandler(BaseHandler):

    route_map = r'/yard/edit/(.*)'

    @authenticated
    @coroutine
    def post(self, id):
        source = self.get_argument('source', None)
        region = self.get_argument('region', None)
        name = self.get_argument('name', None)
        phone = self.get_argument('phone', None)
        address = self.get_argument('address', None)

        yard = yield Yard.objects.get(ObjectId(id))
        if source is not None:
            yard.source = source
        if region is not None:
            yard.region = region
        if name is not None:
            yard.name = name
        if phone is not None:
            yard.phone = phone
        if address is not None:
            yard.address = address

        yield yard.save()
        return self.write_son({})


class YardDeleteHandler(BaseHandler):

    route_map = r'/yard/delete/(.*)'

    @authenticated
    @coroutine
    def post(self, id):
        yard = yield Yard.objects.get(ObjectId(id))
        yield yard.delete()
        return self.write_son({})
