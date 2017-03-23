#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#  main
# ------------------------------------------------------------------------------
from util import authorize, RestException, which_method, rest_response
from mongo import connect
import logging
log = logging.getLogger()
log.setLevel(logging.INFO)


def get_category(event):
    """
    Category lookup.
    If category_id exists in url path lookup by id
    else find all categories
    :param event: dict() aws api gateway object
    :return: list() or dict()  many or single category
    """
    category_id = event['path'].get('category_id')
    if category_id:
        return connect('category').find_by_id(category_id)
    return [x for x in connect('category').find()]


def post_category(event):
    """
    Add a category to mongo collection
    :param event: dict() aws api gateway object
    :return: str() inserted id
    """
    inserted = connect('category').insert_one(event['payload'])
    return inserted.inserted_id


@authorize
def category(event, context, exception=None):
    """
    Operations on categories. Lookup or add
    :param event: dict() aws api gateway object
    :param context: dict() aws api context object
    :param exception: RestException() if client isn't authorized
    :return: dict() rest_response()
    """
    if isinstance(exception, RestException):
        log.exception(exception.message)
        return exception.response
    try:
        response = {
            'POST': post_category,
            'GET': get_category
        }[which_method(event)](event)
        return rest_response(
            payload=response,
            error=False,
            response_status=True if response else False,
            status_code=200 if response else 404
        )
    except RestException as e:
        return e.response
    except Exception as e:
        log.exception(e)
        return e
