# -*- coding: utf-8 -*-

import json
import inspect
from datetime import datetime, date
from bson.objectid import ObjectId


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, date):
            return obj.isoformat()
        elif isinstance(obj, ObjectId):
            return str(obj)
        elif hasattr(obj, 'to_dict') and inspect.ismethod(obj.to_dict):
            return obj.to_dict()
        return json.JSONEncoder.default(self, obj)
