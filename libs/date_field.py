#!/usr/bin/env python
# -*- coding: utf-8 -*-

import six

from datetime import datetime, date

from motorengine.fields.base_field import BaseField

FORMAT = "%Y-%m-%d"


class DateField(BaseField):

    '''
    Field responsible for storing dates.

    Usage:

    .. testcode:: modeling_fields

        date = DateField(required=True, auto_now_on_insert=True,
                        auto_now_on_update=True)

    Available arguments (apart from those in BaseField):

    * `auto_now_on_insert`
        - When an instance is created sets the field to datetime.now().date
    * `auto_now_on_update`
        - Whenever the instance is saved the field value gets updated to
        datetime.now().date
    '''

    def __init__(self, auto_now_on_insert=False, auto_now_on_update=False,
                 *args, **kw):
        super(DateField, self).__init__(*args, **kw)
        self.auto_now_on_insert = auto_now_on_insert
        self.auto_now_on_update = auto_now_on_update

    def get_value(self, value):
        if self.auto_now_on_insert and value is None:
            return datetime.now().date()

        return value

    def to_son(self, value):
        if self.auto_now_on_update:
            return datetime.now().date()

        if isinstance(value, six.string_types):
            return datetime.strptime(value, FORMAT).date()

        return value

    def from_son(self, value):
        if value is None or isinstance(value, date):
            return value

        return datetime.strptime(value, FORMAT).date()

    def validate(self, value):
        return value is None or isinstance(value, date)
