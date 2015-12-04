#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bson.objectid import ObjectId

from motorengine.fields.base_field import BaseField


class ObjectIdField(BaseField):
    '''
        Field responsible for ObjectId.
    '''

    def validate(self, value):
        return isinstance(value, ObjectId)
