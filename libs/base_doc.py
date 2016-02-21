# coding=utf-8

from motorengine.document import Document
from motorengine.fields import DateTimeField
from motorengine.fields import StringField

import settings


class BaseDoc(Document):

    SOURCE_LIST = ['京东', '天猫', '苏宁', '一号店', '飞牛']

    STATUS_LIST = ['ERROR', 'ACTIVE', 'DELETED']

    status = StringField(db_field='status', max_length=20, required=True,
                                default="ACTIVE")
    create_at = DateTimeField(auto_now_on_insert=True)
    update_at = DateTimeField(
        auto_now_on_insert=True, auto_now_on_update=True)
