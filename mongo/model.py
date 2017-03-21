#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#  model
# ------------------------------------------------------------------------------
from pymongo.collection import Collection


class BaseModel(Collection):
    pass


class Acl(BaseModel):
    __collection__ = 'acl'

    def find_by_auth(self, key):
        doc = self.find_one({'_id': key, "active": 1})
        if doc:
            doc.pop('_id', None)
            return doc
        return {}


class Category(BaseModel):
    __collection__ = 'category'

    def find(self, *args, **kwargs):
        return super(Category).find(*args, **kwargs)

    def find_one(self, filter=None, *args, **kwargs):
        return super(Category).find(filter=filter, *args, **kwargs)
