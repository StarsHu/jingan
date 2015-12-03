# coding=utf-8

from motorengine.document import Document
from motorengine.fields import DateTimeField

import settings


class BaseDoc(Document):

    create_at = DateTimeField(auto_now_on_insert=True)
    update_at = DateTimeField(
        auto_now_on_insert=True, auto_now_on_update=True)
