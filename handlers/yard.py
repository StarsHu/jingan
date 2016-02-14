# coding=utf-8

from tornado.web import authenticated
from tornado.gen import coroutine
from bson.objectid import ObjectId

from models import Yard
from motorengine.query_builder.node import Q
from motorengine import DESCENDING
from libs.base_handler import BaseHandler, authorized
from libs.form_error import FormError


class YardPageListHandler(BaseHandler):

    route_map = r'/yard/list'

    @authenticated
    @authorized(['admin'])
    @coroutine
    def get(self):
        query = Q(status='ACTIVE')
        if self.query:
            q = '.*%s.*' % self.query
            query = query & (
                Q({"name": {'$regex': q}})
                | Q({"region": {'$regex': q}})
                | Q({"phone": {'$regex': q}})
                | Q({"address": {'$regex': q}})
            )
        qs = Yard.objects.filter(query).order_by('create_at',
                                                 direction=DESCENDING)
        total = yield qs.count()
        if self.page:
            skip = self.count_per_page * (self.page - 1)
            limit = self.count_per_page
            qs = qs.skip(skip).limit(limit)
        yards = yield qs.find_all()
        self.context['total'] = total / self.count_per_page
        self.context['yards'] = yards
        self.render('yard_list.html', **self.context)


class YardCreateHandler(BaseHandler):

    route_map = r'/yard/create'

    @authenticated
    @authorized(['admin'])
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

        return self.write_son({
            'redirect': '/yard/list',
        })


class YardUpdateHandler(BaseHandler):

    route_map = r'/yard/update/(.*)'

    @authenticated
    @authorized(['admin'])
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
    @authorized(['admin'])
    @coroutine
    def post(self, id):
        yard = yield Yard.objects.get(ObjectId(id))
        yield yard.delete()
        return self.write_son({})
