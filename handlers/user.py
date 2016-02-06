# coding=utf-8

from tornado.web import authenticated
from tornado.gen import coroutine
from bson.objectid import ObjectId

from models import User, Role
from motorengine.query_builder.node import Q
from motorengine import DESCENDING
from libs.base_handler import BaseHandler
from libs.form_error import FormError


class UserPageListHandler(BaseHandler):

    route_map = r'/user/list'

    @authenticated
    @coroutine
    def get(self):
        query = Q(status='ACTIVE')
        if self.query:
            q = '.*%s.*' % self.query
            query = query & Q({"name": {'$regex': q}})
        qs = User.objects.filter(query).order_by('create_at',
                                                 direction=DESCENDING)
        total = yield qs.count()
        if self.page:
            skip = self.count_per_page * (self.page - 1)
            limit = self.count_per_page
            qs = qs.skip(skip).limit(limit)
        users = yield qs.find_all()
        roles = yield Role.objects.find_all()

        self.context['total'] = total
        self.context['users'] = users
        self.context['roles_display'] = { r.key: r.name for r in roles }
        self.render('user_list.html', **self.context)


class UserCreateHandler(BaseHandler):

    route_map = r'/user/create'

    @authenticated
    @coroutine
    def post(self):
        name = self.get_argument('name')
        password_raw = self.get_argument('password')
        role_key = self.get_argument('role_key')

        role = yield Role.objects.get(key=role_key)
        if not role:
            return self.write_son({
                'errors': [FormError("角色不存在. 请联系管理员.")],
            })
        yield User(name=name,
                   password=User.encode_raw_password(password_raw),
                   role=role
                   ).save()

        return self.write_son({
            'redirect': '/user/list',
        })


class UserUpdateHandler(BaseHandler):

    route_map = r'/user/update/(.*)'

    @authenticated
    @coroutine
    def post(self, id):
        source = self.get_argument('source', None)
        region = self.get_argument('region', None)
        name = self.get_argument('name', None)
        phone = self.get_argument('phone', None)
        createress = self.get_argument('createress', None)

        user = yield User.objects.get(ObjectId(id))
        if source is not None:
            user.source = source
        if region is not None:
            user.region = region
        if name is not None:
            user.name = name
        if phone is not None:
            user.phone = phone
        if createress is not None:
            user.createress = createress

        yield user.save()
        return self.write_son({})


class UserDeleteHandler(BaseHandler):

    route_map = r'/user/delete/(.*)'

    @authenticated
    @coroutine
    def post(self, id):
        user = yield User.objects.get(ObjectId(id))
        yield user.delete()
        return self.write_son({})
