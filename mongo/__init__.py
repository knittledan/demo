#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#  __init__.py
# ------------------------------------------------------------------------------
import inspect
from pymongo import MongoClient
from mongo import model
from config import connections


def connect(collection):
    """
    Returns a user defined model with it connected to the respected remote
    mongo db and collection.
    :param collection: str() collection to perform operations on
    :return: Collection()
    """

    class Mongo(object):
        __slots__ = ('collection',)
        PREFIX = 'mongo_cache'
        CACHE  = {}

        def __init__(self, _collection):
            self.collection = _collection

        @property
        def __model(self):
            """
            Finds the user defined model based on the collection you're trying
            to connect to.
            :return: obj() from model package
            """
            for name, obj in inspect.getmembers(model, inspect.isclass):
                if getattr(obj, '__collection__', False) == self.collection:
                    return obj
            raise Exception("There's no model defined for %s" % collection)

        @property
        def model(self):
            """
            Makes the mongo connection then assigns it to a user defined model.
            :return: Collection()
            """
            c = self.connections
            if self.collection in c:
                return c[self.collection]
            client = MongoClient(**self.client)
            if not client[self.db].authenticate(**self.auth):
                raise Exception("%s couldn't authenticate to %s" %
                                (client, self.db))
            self.__assign_model_to_connection(client, c)
            return c[self.collection]

        def __assign_model_to_connection(self, client, connections):
            """
            Associates a mongo Collection() to a user defined model.
            :param client: MongoClient() connection
            :param connections: dict() of connections cache
            """
            db = client[self.db]
            model = db[self.collection]
            model.__class__ = self.__model
            connections[self.collection] = model

        @property
        def _conf(self):
            """
            Calls the super cache to read in mongo settings
            :return: dict() mongo config, connection & collection settings
            """
            conf = connections.get(self.collection)
            if not conf:
                raise Exception("%s is missing from config" % collection)
            return conf

        @property
        def client(self):
            """
            Returns the client connection params from the .json
            :return: dict() host, port, connect
            """
            return self._conf['client']

        @property
        def auth(self):
            """
             Returns the auth params from the .json
             :return: dict() name, password, mechanism, source
             """
            return self._conf['auth']

        @property
        def db(self):
            """
             Returns the db params from the .json
             :return: dict() db name
             """
            return self._conf['db']

        @property
        def connections(self):
            """
            Used to cache already instantiated connections to a collection
            :return: Collection() mongo collection obj
            """
            if not self._conf.get('c'):
                self._conf['c'] = dict()
            return self._conf['c']
    return Mongo(collection).model