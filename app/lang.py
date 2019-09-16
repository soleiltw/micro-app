from enum import Enum

from bottle import request


class Lang(Enum):
    NOT_FOUND = (
        '您请求的资源不存在',
        'Not found')

    REQUEST_INVALID = (
        '无效的请求',
        'Invalid request',
    )

    PARAM_INVALID = (
        '无效的参数',
        'Invalid params.')

    INTERNAL_ERROR = (
        '内部错误',
        'Internal error.')

    UNAUTHENTICATED = (
        '请您先登陆',
        'Please login')

    def __init__(self, lang_zh, lang_id=''):
        self.zh = lang_zh
        self.id = lang_id
        self.default = self.id

    @property
    def auto(self):
        accept_language = request.headers.get('Accept-Language')
        if accept_language is None:
            return self.default
        accept_language = accept_language.lower()
        if accept_language.startswith('zh'):
            return self.zh
        if accept_language.startswith('id'):
            return self.id
        return self.default
