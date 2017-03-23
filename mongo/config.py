#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#  config
# ------------------------------------------------------------------------------
connections = {
    "category": {
        "client": {
            "host": "54.219.140.116",
            "port": 27017,
            "connect": False
        },
        "auth": {
            "name": "demo_user",
            "password": "76tfbutfhTRFu76rfvbUY^TRdcv",
            "mechanism": "SCRAM-SHA-1",
            "source": "admin"
        },
        "db": "data"
    },
    "acl": {
        "client": {
            "host": "54.219.140.116",
            "port": 27017,
            "connect": False
        },
        "auth": {
            "name": "demo_user",
            "password": "76tfbutfhTRFu76rfvbUY^TRdcv",
            "mechanism": "SCRAM-SHA-1",
            "source": "admin"
        },
        "db": "data"
    }
}