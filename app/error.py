import json
import logging

import bottle
from bottle import response

app = bottle.default_app()


def error_500_handler(error):
    exception = error.exception

    result = {'error': {'message': error.body}}

    # if isinstance(exception, peewee.DoesNotExist):
    #     response.status = 404
    #     result['error']['message'] = Lang.NOT_FOUND.auto

    # elif isinstance(exception, voluptuous.error.Error):
    #     # 参数校验错误
    #     errors = []
    #     if isinstance(exception, voluptuous.error.MultipleInvalid):
    #         errors = exception.errors
    #     elif isinstance(exception, voluptuous.error.Invalid):
    #         errors = [exception]
    #
    #     response.status = 400
    #     result['error']['message'] = Lang.PARAM_INVALID.auto
    #     invalid_params = ['.'.join(map(str, e.path))
    #                       for e in errors if e.path]
    #     if invalid_params:
    #         result['error']['params'] = invalid_params

    response.content_type = 'application/json'
    logging.error('error occured. response: %s', result)
    return json.dumps(result)


def default_error_handle(error: bottle.HTTPError):
    response.content_type = 'application/json'
    return json.dumps({'error': {'message': error.body}})


def register_error_handler():
    app.error_handler[400] = default_error_handle
    app.error_handler[401] = default_error_handle
    app.error_handler[403] = default_error_handle
    app.error_handler[404] = default_error_handle
    app.error_handler[500] = error_500_handler
