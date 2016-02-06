# -*- coding: utf-8 -*-

import hashlib
from motorengine import fields

import settings
from libs.base_doc import BaseDoc
from libs.object_id_field import ObjectIdField
from libs.date_field import DateField


class Role(BaseDoc):

    __collection__ = 'role'

    STATUS_LIST = ['ERROR', 'ACTIVE', 'DELETED']
    key = fields.StringField(db_field='key', max_length=50, unique=True,
                             required=True)
    name = fields.StringField(db_field='name', max_length=50, required=True)


class User(BaseDoc):

    __collection__ = 'user'
    __lazy__ = False

    STATUS_LIST = ['ERROR', 'ACTIVE', 'DELETED']

    name = fields.StringField(db_field='name', max_length=50, unique=True,
                              required=True)
    password = fields.StringField(db_field='password', max_length=50,
                                  required=True)
    last_login = fields.DateTimeField(db_field='last_login', required=False)
    role = fields.ReferenceField(reference_document_type=Role)

    @classmethod
    def encode_raw_password(cls, password):
        m = hashlib.md5()
        m.update(password.encode('utf-8'))
        return m.hexdigest()

    def check_raw_password(self, password):
        return self.check_encoded_password(self.encode_raw_password(password))

    def check_encoded_password(self, password):
        if password == self.password:
            return True
        else:
            return False

    def set_password(self, password):
        self.password = self.encode_raw_password(password)

    def get_role(self):
        return Role.objects.get(self.role_id)


class Product(BaseDoc):

    __collection__ = 'product'

    sku = fields.StringField(db_field='sku', max_length=50, unique=True,
                             required=True)
    name = fields.StringField(db_field='name', max_length=200, required=True)
    id_from_source = fields.StringField(db_field='id_from_source', max_length=50)
    price_for_ref = fields.DecimalField(db_field='price_for_ref', required=True,
                                        default=0.0)


class Yard(BaseDoc):

    __collection__ = 'yard'

    source = fields.StringField(db_field='source', max_length=20, required=True)
    region = fields.StringField(db_field='region', max_length=20,
                                required=True, default='')
    name = fields.StringField(db_field='name', max_length=200, required=True)
    phone = fields.StringField(db_field='phone', max_length=100, required=True)
    address = fields.StringField(db_field='address', max_length=200,
                                 required=True, default='')


class Order(BaseDoc):
    '''
    the sub_orders format:
        [
            {
                id_from_source: String,
                dest_from_source: String,
                items: {
                    "product": Product,
                    "count": Int,
                    "price": Decimal,
                }
            }
        ...
        ]
    '''

    __collection__ = 'order'

    uuid = fields.StringField(db_field='uuid', max_length=50, unique=True,
                              required=True)
    source = fields.StringField(db_field='source', max_length=20, required=True)
    seller = fields.StringField(db_field='seller', max_length=20, required=True)
    yard = fields.EmbeddedDocumentField(embedded_document_type=Yard)
    deliver_at = DateField(db_field='deliver_at', required=False)
    sub_orders = fields.JsonField(db_field='sub_orders', required=True,
                                  default=dict())

