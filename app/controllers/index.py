import gzip
import json
import logging

from bottle import post, request, get


@get('/')
def index():
    logging.debug('Healthy check.')
    pass  # healthy check


@get('/healthy')
def index():
    logging.debug('Healthy check.')
    pass  # healthy check


@post('/v1/echo')
def post_index():
    ua = request.headers.get('Authorization', '')
    logging.debug('Authorization: %s', ua)

    content_encoding = request.headers.get('Content-Encoding', '').lower()

    body = request.body.read()
    if content_encoding == 'gzip':
        body = gzip.decompress(body)
    body = body.decode('utf-8')

    data_json = json.loads(body)
    logging.debug('Data keys: %s', data_json.keys())

    result = {'result': 'OK'}
    return result
