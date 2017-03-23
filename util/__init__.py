#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#  __init__.py
# ------------------------------------------------------------------------------


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
        self.message = payload
        self.status_code = status_code
        self.payload = payload
        self.error = error
        self.response_status = response_status
        self.response = rest_response(payload, status_code, error,
                                      response_status)


def auth_key(event):
    """
    Pulls the authorization key from the header.
    :param event: dict() aws api gateway request data
    :return: str() auth key
    """
    headers = event.get('header')
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


def is_authorized(acl, event, context):
    """

    :param acl: dict() result from mongo acl
    :param event: dict() aws api gateway request data
    :param context: obj() aws api gateway context
    """
    func_name   = context.function_name
    http_method = event['context']['http_method']
    if func_name not in acl:
        raise RestException("Forbidden", 403)
    if http_method not in acl[func_name]:
        raise RestException("Forbidden method. You're allowed %s"
                            % ', '.join(acl[func_name]), 403)


def authorize(func):
    """
    Decorator to verify authentication for each method call
    :param func: func() decorated function
    :return: any() function results
    """
    def func_wrapper(*args):
        from mongo import connect
        event   = args[0]
        context = args[1]
        e = None
        try:
            acl = connect('acl').find_by_auth(auth_key(event))
            if not acl:
                e = RestException("Unauthorized", 403)
                is_authorized(acl, event, context)
        except RestException as e:
            return func(*args, exception=e)
        return func(*args, exception=e or None)
    return func_wrapper


def which_method(event):
    """
    Pulls the request method used by the client
    :param event: dict() aws api gateway request data
    :return: str() method
    """
    return event['context']['http_method']