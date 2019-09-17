import gzip
import json
import logging

from bottle import post, request, get


@get('/')
def index():
    """
    @api {get} / Easy check
    @apiName Easy for health check.
    @apiGroup Healthy
    @apiVersion 1.0.0

    @apiSuccessExample {json} Success-Response:
    HTTP/1.1 200 OK
    Content-Length: 0
    Content-Type: text/html; charset=UTF-8
    Date: Mon, 16 Sep 2019 09:32:46 GMT
    Server: gunicorn/19.9.0
    """
    logging.debug('Healthy check.')
    pass  # healthy check


@get('/healthy')
def index():
    """
    @api {get} /healthy Another easy check
    @apiName A path for another health check.
    @apiGroup Healthy
    @apiVersion 1.0.0

    @apiSuccessExample {json} Success-Response:
    HTTP/1.1 200 OK
    Content-Length: 0
    Content-Type: text/html; charset=UTF-8
    Date: Mon, 16 Sep 2019 09:32:46 GMT
    Server: gunicorn/19.9.0
    """
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
