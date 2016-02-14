# coding=utf-8

from tornado.web import authenticated
from tornado.gen import coroutine
from bson.objectid import ObjectId

from models import Product
from motorengine.query_builder.node import Q
from motorengine import DESCENDING
from libs.base_handler import BaseHandler, authorized
from libs.form_error import FormError


class ProductPageListHandler(BaseHandler):

    route_map = r'/product/list'

    @authenticated
    @authorized(['admin'])
    @coroutine
    def get(self):
        query = Q(status='ACTIVE')
        if self.query:
            q = '.*%s.*' % self.query
            query = query & (
                Q({"sku": {'$regex': q}})
                | Q({"name": {'$regex': q}})
                | Q({"id_from_source": {'$regex': q}})
                | Q({"price_for_ref": {'$regex': q}})
            )
        qs = Product.objects.filter(query).order_by('create_at',
                                                    direction=DESCENDING)
        total = yield qs.count()
        if self.page:
            skip = self.count_per_page * (self.page - 1)
            limit = self.count_per_page
            qs = qs.skip(skip).limit(limit)
        products = yield qs.find_all()
        self.context['total'] = total / self.count_per_page
        self.context['products'] = products
        self.render('product_list.html', **self.context)


class ProductCreateHandler(BaseHandler):

    route_map = r'/product/create'

    @authenticated
    @authorized(['admin'])
    @coroutine
    def post(self):
        sku = self.get_argument('sku')
        name = self.get_argument('name')
        id_from_source = self.get_argument('id_from_source', '')
        price_for_ref = self.get_argument('price_for_ref', 0.0)

        product = Product(
            sku=sku,
            name=name,
            id_from_source=id_from_source,
            price_for_ref=price_for_ref,
        )
        yield product.save()

        return self.write_son({
            'redirect': '/product/list',
        })


class ProductUpdateHandler(BaseHandler):

    route_map = r'/product/update/(.*)'

    @authenticated
    @authorized(['admin'])
    @coroutine
    def post(self, id):
        sku = self.get_argument('sku', None)
        name = self.get_argument('name', None)
        id_from_source = self.get_argument('id_from_source', None)
        price_for_ref = self.get_argument('price_for_ref', None)

        product = yield Product.objects.get(ObjectId(id))
        if sku is not None:
            product.sku = sku
        if name is not None:
            product.name = name
        if id_from_source is not None:
            product.id_from_source = id_from_source
        if price_for_ref is not None:
            product.price_for_ref = price_for_ref

        yield product.save()
        return self.write_son({})


class ProductDeleteHandler(BaseHandler):

    route_map = r'/product/delete/(.*)'

    @authenticated
    @authorized(['admin'])
    @coroutine
    def post(self, id):
        product = yield Product.objects.get(ObjectId(id))
        yield product.delete()
        return self.write_son({})
