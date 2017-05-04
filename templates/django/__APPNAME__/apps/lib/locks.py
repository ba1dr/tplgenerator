
import socket

from enum import Enum

from .semaphores import Semaphore

THISHOST = socket.getfqdn()  # for local locks


class KnownLocks(Enum):
    CUSTOM_LOCAL_LOCK = {'name': 'custom_lock_%s', 'scope': 'local'}
    CUSTOM_GLOBAL_LOCK = {'name': 'custom_lock_%s', 'scope': 'global'}


class _LockerMeta(type):

    def __getattr__(cls, name):
        if name in KnownLocks.__members__:
            lockitem = getattr(KnownLocks, name).value
            lockname = lockitem['name']
            if lockitem['scope'] == 'local':
                lockname = "%s::%s" % (THISHOST, lockitem['name'])
            return lockname
        return getattr(cls, name)


class Locker(object, metaclass=_LockerMeta):

    @classmethod
    def get_all_semaphores(cls, show_all=False, local=False):
        sclient = Semaphore.new_client()
        smprefix = "%s::" % Semaphore.PREFIX
        if local:
            smprefix += "%s::" % (THISHOST)
        smp_pattern = "%s*" % smprefix
        klist = []
        for k in sclient.keys(smp_pattern):
            key = k.decode()[len(smprefix):]
            value = sclient.get(k).decode()
            if value and value.isdigit():
                if show_all or value not in [0, '0']:
                    # klist.append((key, cls.explain(k)))
                    klist.append((key, value))
        return klist

    @classmethod
    def clear_bymask(cls, pattern):
        sclient = Semaphore.new_client()
        kmask = "%s::%s" % (Semaphore.PREFIX, pattern)
        cnt = 0
        for k in sclient.keys(kmask):
            sclient.delete(k)
            cnt += 1
        return cnt
