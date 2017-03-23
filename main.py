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
    category_id = event['path'].get('category_id')
    if category_id:
        return connect('category').find_by_id(category_id)
    return [x for x in connect('category').find()]


def post_category(event):
    inserted = connect('category').insert_one(event['payload'])
    return inserted.inserted_id


@authorize
def category(event, context, exception=None):
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
            response_status=True,
            status_code=100
        )
    except RestException as e:
        return e.response
    except Exception as e:
        return e


# if __name__ == "__main__":
#     aws_event = {
#         'headers': {'Authorization': 'Bearer 4bb074faf1b1f7d88910d94debed11e3'},
#         'path': {},
#         'payload': {'_id': 'Festivals', 'hero': 'http://s1.evcdn.com/store'
#                                                 '/festivals/music-festivals/fest-portal-images/hub-hero.jpg'},
#         'context': {'http_method': 'POST'}
#     }
#     aws_context = type('', (object,), {'function_name': 'category'})()
#     print(category(aws_event, aws_context))
