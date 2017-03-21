#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#  __init__.py
# ------------------------------------------------------------------------------
from mongo import connect


def rest_response(payload, status_code, error, response_status):
    """
    Use this to return a json response to the requesting client.
    :param payload: dict() or str() or anything that can be encoded.
    :param status_code: int() internal status code
    :param error: bool() if the request caused an error
    :param response_status: bool() is the request was a success.
    :return: dict() payload
    """
    return {
        'payload': payload,
        'status_code': status_code,
        'error': error,
        "response_status": response_status
    }


class RestException(Exception):
    """
    Raises an exception that immediately constructs a response to the client
    """

    def __init__(self, payload, status_code, error=True, response_status=False):
        self.status_code = status_code
        self.payload = payload
        self.error = error
        self.response_status = response_status
        self.response = rest_response(payload, status_code, error,
                                      response_status)


def auth_key(event):
    headers = event.get('headers')
    if not headers:
        raise RestException("Headers are missing", 400)
    auth = headers.get('Authorization')
    if not auth:
        raise RestException('Header Authorization is missing', 400)
    if not auth.lower().startswith('bearer '):
        raise RestException("Authorization missing Bearer keyword", 400)
    auth = auth.replace('Bearer ', '')
    auth = auth.replace('bearer ', '')
    return auth.strip()


def authorize(func):
    def func_wrapper(*args):
        event = args[0]
        if not connect('acl').find_by_auth(auth_key(event)):
            e = RestException("Unauthorized", 401)
        return func(*args, exception=e or None)
    return func_wrapper
