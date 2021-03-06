#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#  model
# ------------------------------------------------------------------------------
from pymongo.collection import Collection
from datetime import datetime

from pymongo.errors import DuplicateKeyError

from util import RestException

def encoder(data):
    if not data:
        return data
    for k, v in data.items():
        if isinstance(v, datetime):
            data[k] = str(v)
    return data


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
    required = ['hero']

    def find(self, *args, **kwargs):
        r = super(Category, self).find(*args, **kwargs)
        return [encoder(x) for x in r]

    def find_by_id(self, category_id):
        r = self.find_one_and_update({'_id': category_id},
                                     {'$inc': {'views': 1}},
                                     return_document=True)
        return encoder(r)

    def find_one(self, filter=None, *args, **kwargs):
        return super(Category, self).find(filter=filter, *args, **kwargs)

    def insert_one(self, document, bypass_document_validation=False):
        missing = [x for x in self.required if x not in document]
        if missing:
            raise RestException('Category must contain required fields %s'
                                % ', '.join(missing), 400)
        document['created'] = datetime.utcnow()
        document['updated'] = datetime.utcnow()
        document['views']   = 0
        state = document.get('active', None)
        document['active']  = True if state is None else state
        try:
            return super(Category, self).insert_one(document,
                                                    bypass_document_validation)
        except DuplicateKeyError:
            raise RestException("Category %s already exists" % document['_id'],
                                400)
