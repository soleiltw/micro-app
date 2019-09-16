import os
from datetime import tzinfo, timedelta
from enum import Enum

import re
from bottle import request


def _plain_args(d, list_fields=None):
    list_fields = list_fields or ()

    result = dict((key, d.getunicode(key)) for key in d)
    for key in list_fields:
        result[key] = d.getall(key)

    return result


def plain_forms(list_fields=None):
    """ Plain POST data. """
    return _plain_args(request.forms, list_fields)


def plain_query(list_fields=None):
    """ Plain GET data """
    return _plain_args(request.query, list_fields)


def plain_params(list_fields=None):
    """ Plain all data """
    return _plain_args(request.params, list_fields)


def mask(s, start=0, end=None, fill_with='*'):
    """ 将指定范围内的字符替换成指定字符，范围规则与 list 切片一致 """
    sl = list(s)
    if end is None:
        end = len(sl)
    sl[start:end] = fill_with * len(sl[start:end])
    return ''.join(sl)


def env_detect():
    env = os.environ.get('APP_ENV')
    if env is None:
        env = 'DEV'
    return env


def request_ip():
    return (request.environ.get('HTTP_X_FORWARDED_FOR') or
            request.environ.get('REMOTE_ADDR'))


class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        return [(e.name, e.value) for e in cls]

    @classmethod
    def values(cls):
        return [e.value for e in cls]


def dt_truncate(dt):
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)


def dt_ceiling(dt):
    return dt.replace(hour=23, minute=59, second=59, microsecond=0)


number_strip_re = re.compile(r'\d+')


def number_strip(m):
    # 印尼的号码有86开头，所以去掉中国 的 86 要跟着 + 一起
    m = m.replace('+86', '')

    # 以下规则，都不考虑中国号码

    # 先取纯数字
    number = ''.join(number_strip_re.findall(m))

    if number.startswith('62'):
        number = number[2:]

    # 所有开头的 0 都不要
    return number.lstrip('0')


class ChinaZone(tzinfo):
    def utcoffset(self, dt):
        return timedelta(hours=+8)

    def tzname(self, dt):
        return "China"

    def dst(self, dt):
        return timedelta(0)
