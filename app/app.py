import bottle
import os
import logging
from importlib import import_module

import sys

from app.error import register_error_handler
from app.utils import env_detect

os.chdir(os.path.dirname(__file__))
app = application = bottle.default_app()


def load_config():
    app.config.load_config('config/base.ini')

    cur_env = env_detect().lower()

    if os.path.exists('config/%s.ini' % cur_env):
        app.config.load_config('config/%s.ini' % cur_env)

    # load config map in k8s
    config_map_path = os.environ.get('APP_CONFIG_MAP_PATH')
    secret_path = os.environ.get('APP_SECRET_PATH')
    for path in (config_map_path, secret_path):
        if not (path and os.path.exists(path)):
            continue

        config_map = {}
        for entry in os.scandir(path):
            if entry.is_file() and not entry.name.startswith('.'):
                with open(entry.path, encoding='utf-8') as f:
                    config_map[entry.name] = f.read().strip()

        if config_map:
            app.config.update(**config_map)


def load_controllers():
    for path in ('app.controllers', 'app.api'):
        root_module = import_module(path)
        file_name = os.path.basename(root_module.__file__)
        if file_name != '__init__.py':
            continue

        root_dir = os.path.dirname(root_module.__file__)
        for c in os.listdir(root_dir):
            head, _ = os.path.splitext(c)
            if not head.startswith('_'):
                import_module(path + '.' + head)


def set_logger():
    default_format = ('[%(asctime)s] [%(levelname)s] '
                      '[%(module)s: %(lineno)d] %(message)s')
    logging_level = app.config.get('logging.level', 'ERROR')
    logging.basicConfig(
        stream=sys.stdout,
        level=getattr(logging, logging_level.upper()),
        format=default_format,
        datefmt='%Y-%m-%d %H:%M:%S %z',
    )


def init_app():
    load_config()
    set_logger()
    load_controllers()
    register_error_handler()
    logging.debug('Init app finished.')
    return app
