#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#  main
# ------------------------------------------------------------------------------
from util import authorize, RestException


@authorize
def category(event, context, exception=None):
    if isinstance(exception, RestException):
        return exception.response


if __name__ == "__main__":
    print(category({'headers': {'Authorization': 'Bearer f3aec113d0dd9e17a435dfa9e246ead0'}},
             {'context': 'somthing'}))
