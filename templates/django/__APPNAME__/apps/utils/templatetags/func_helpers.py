# -*- coding: utf-8 -*-

"""
    In this file we have some functions to bypass limitations to:
        call methods with parameters and with multiple parameters too.

    For example, if you need to call in the template:
        myobject.mymethod(1, 2, 3)
    Use the following syntax:
        {{ myobject|arg:1|arg:2|arg:3|call:'mymethod' }}
"""

from django import template

register = template.Library()


@register.filter
def arg(prevs, newarg):
    """ Joins arguments to list """
    retval = prevs
    if not isinstance(retval, list):
        retval = [retval]
    return retval + [newarg]


@register.filter
def call(objs, func=None):
    """ Call instance's method with parameters.
        First parameter should be either [instance, argument1, argument2, ...] or instance itself.
        Will be called as: instance.func(argument1, argument2, ...)
    """
    obj = objs
    args = []
    if isinstance(objs, list):
        obj = objs[0]
        args = objs[1:]
    func = getattr(obj, func)
    return func(*args)
