# -*- coding: utf-8 -*-

import os
import time
from functools import wraps

from django.conf import settings

from .redis import create_global_client

__all__ = ('Semaphore', )


class SemaphoreAcquireFailed(Exception):
    pass


def getint(value):
    if not value:
        return 0
    if isinstance(value, int):
        return value
    if isinstance(value, bytes) and value.isdigit():
        return int(value)
    return 0


def classinstmethod(func):
    """ Allows the wrapped method to be called both ways - as class's method or as instance's method """
    @wraps(func)
    def wrapper(*args, **kwargs):
        klass = None
        klassname = func.__qualname__.split('.')[0]
        if args:
            firstarg = args[0]
            if firstarg.__class__.__name__ == klassname:
                klass = firstarg
                args = args[1:]
        klass = klass or func.__globals__[klassname]
        return func(klass, *args, **kwargs)
    return wrapper


def to_list(o):
    if isinstance(o, list):
        return o
    return [o]


def defraise(error):
    raise ValueError(error)


class Semaphore(object):
    """ Class to manipulate semaphores in Redis """
    WAIT_PAUSE = 2  # seconds
    PREFIX = "semaphore"

    @classmethod
    def get_name(cls, name):
        if cls.PREFIX and not name.startswith(cls.PREFIX + '::'):
            return "%s::%s" % (cls.PREFIX, name)
        return name

    @classmethod
    def new_client(cls):
        # return redis.StrictRedis.from_url(settings.SEMAPHORES_REDIS_URL)
        # if not globalclient:
        return create_global_client()
        # globalclient = redis.StrictRedis.from_url(settings.SEMAPHORES_REDIS_URL)
        # return globalclient

    def __init__(self, names, acquire=False, client=None, acquire_wait=True):
        self.client = client or self.new_client()
        self.names = to_list(names)
        self.do_acquire = acquire
        self.acquire_wait = acquire_wait

    @classinstmethod
    def check_exists(cls, names=None, client=None):
        """ Returns True if semaphore count > 0 """
        client = client or getattr(cls, 'client', None) or cls.new_client()
        names = names or getattr(cls, 'names', None) or defraise("names are not passed")
        for name in to_list(names):
            if int(cls.get(name, client=client) or 0) > 0:
                return True
        return False

    @classinstmethod
    def wait_release(cls, names=None, timeout=None, client=None):
        c = 0
        client = client or getattr(cls, 'client', None) or cls.new_client()
        names = names or getattr(cls, 'names', None) or defraise("names are not passed")
        while cls.check_exists(names, client=client):
            time.sleep(cls.WAIT_PAUSE)
            if timeout:
                c += cls.WAIT_PAUSE
                if c >= timeout:
                    return False  # cannot not wait
        return True

    @classinstmethod
    def clear(cls, names=None, client=None):
        client = client or getattr(cls, 'client', None) or cls.new_client()
        names = names or getattr(cls, 'names', None) or defraise("names are not passed")
        for name in to_list(names):
            client.set(cls.get_name(name), 0)

    @classinstmethod
    def get(cls, name, client=None):
        """ Returns count of acquired semafores """
        client = client or getattr(cls, 'client', None) or cls.new_client()
        return getint(client.get(cls.get_name(name)))

    @classinstmethod
    def set(cls, name, client=None):  # actually increment
        client = client or getattr(cls, 'client', None) or cls.new_client()
        return client.incr(cls.get_name(name))

    @classinstmethod
    def force_set(cls, name, value=1, client=None):  # set the value
        client = client or getattr(cls, 'client', None) or cls.new_client()
        return client.set(cls.get_name(name), value)

    @classinstmethod
    def unset(cls, name, client=None):
        client = client or getattr(cls, 'client', None) or cls.new_client()
        return client.decr(cls.get_name(name))

    @classinstmethod
    def acquire(cls, names=None, timeout=None, client=None):
        """ Allows only one instance of the given semaphore.
            Tries to raise each of the given names and returns false if any of them has been already set.
            Do not forget to call clear() or unset() after the resource is released
            After timeout seconds the key gets expired (if set)
        """
        client = client or getattr(cls, 'client', None) or cls.new_client()
        names = names or getattr(cls, 'names', None) or defraise("names are not passed")
        to_rollback = []
        for name in to_list(names):
            to_rollback.append(name)
            vvv = cls.set(name, client=client)
            if vvv > 1:  # one has been already set
                for rbname in to_rollback:
                    cls.unset(rbname, client=client)
                return False
        if timeout:
            for name in to_list(names):
                client.expire(name, timeout)
        return True

    def __enter__(self):
        if self.do_acquire:
            if self.acquire_wait:
                self.wait_release()
                while not self.acquire():
                    time.sleep(self.WAIT_PAUSE)
            else:
                if not self.acquire():
                    raise SemaphoreAcquireFailed()
        else:
            for name in self.names:
                self.set(name, client=self.client)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        for name in self.names:
            self.unset(name, client=self.client)
        return True if exc_type is None else False
