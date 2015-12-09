# -*- coding: utf-8 -*-


class FormError(object):

    def __init__(self, message='', field_name=''):
        self.message = message
        self.field_name = field_name

    def to_dict(self):
        return self.__dict__
