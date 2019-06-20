# -*- coding: utf-8 -*-

"""
    Function import_settings() will load config file in yaml/json format into the caller's local namespace
    See https://github.com/ba1dr/dynsettings
"""

import os
import sys
import yaml
# import json


def import_settings(fname="settings.yaml", defaults=None):
    ydata = load_settings(fname, defaults)
    # if not os.path.exists(fname):
    #     return
    flocals = sys._getframe().f_back.f_locals
    # mname = sys._getframe().f_back.f_globals['__name__']
    # ydata = []
    # with open(fname, 'r') as ysfile:
    #     if fname.endswith('.yaml'):
    #         ydata = yaml.load(ysfile.read())
    #     elif fname.endswith('.json'):
    #         ydata = json.loads(ysfile.read())
    if ydata:
        for p in ydata:
            pname = p
            pvalue = None
            if isinstance(ydata, list):
                if isinstance(p, dict):
                    pname = p.keys()[0]
                    pvalue = p[pname]
            elif isinstance(ydata, dict):
                pname = p
                pvalue = ydata[pname]
            else:
                # print("Incorrect type")
                break
            # print("Define %s=%s" % (pname, pvalue))
            # globals()[pname] = pvalue
            # setattr(sys.modules[mname], pname, pvalue)
            flocals[pname] = pvalue


def _dictmerge(d1, d2):
    """ Recursive merges d2 into d1 if they are dictionaries (by keys), otherwise returns d2 """
    if isinstance(d1, dict) and isinstance(d2, dict):
        rd = d1
        for k in d2:
            if k in d1:
                rd[k] = _dictmerge(d1[k], d2[k])
            else:
                rd[k] = d2[k]
        return rd
    return d2


def dict_chainget(obj, *chain):
    """ Get the value from dictionary 'obj' one-by one in chain """
    if not chain:
        return obj
    if not isinstance(obj, dict):
        return None
    if chain[0] not in obj:
        return None
    return dict_chainget(obj[chain[0]], *chain[1:])


def _get_fcontent(fname):
    ydata = {}
    if not fname or not os.path.exists(fname):
        return {}
    with open(fname, 'r') as ysfile:
        if fname.endswith('.yaml'):
            ydata = yaml.load(ysfile.read(), Loader=yaml.FullLoader)
        elif fname.endswith('.json'):
            ydata = json.loads(ysfile.read())
    return ydata


def load_settings(settings_file='settings.yaml', defaultsettings_file='settings.default.yaml'):
    CUR_DIR = os.path.dirname(os.path.abspath(__file__))
    _defaultsettings_file = defaultsettings_file
    if _defaultsettings_file and not _defaultsettings_file.startswith('/'):  # not absolute path
        _defaultsettings_file = os.path.join(CUR_DIR, _defaultsettings_file)
    _settings_file = settings_file
    if not _settings_file.startswith('/'):  # not absolute path
        _settings_file = os.path.join(CUR_DIR, _settings_file)

    ds = _get_fcontent(_defaultsettings_file)
    s = _get_fcontent(_settings_file)
    s = _dictmerge(ds, s)
    return s
