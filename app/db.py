import os

import bottle
from bottle import hook
from peewee import MySQLDatabase

from app.utils import ChinaZone

db = MySQLDatabase(None)


@hook('before_request')
def _connect_db():
    db.connect()


@hook('after_request')
def _close_db():
    if not db.is_closed():
        db.close()


def init():
    app = bottle.default_app()

    app.config.setdefault('db.read_timeout', 20)
    app.config.setdefault('db.write_timeout', 20)
    db_password = os.environ.get('DB_PASSWORD') or app.config['db.password']

    db.init(
        app.config['db.database'],
        host=app.config['db.host'],
        user=app.config['db.user'],
        port=int(app.config['db.port']),
        charset=app.config['db.charset'],
        password=db_password,
        autocommit=True,  # 连接mysql 时是否使用autocommit 模式
        read_timeout=app.config['db.read_timeout'],
        write_timeout=app.config['db.write_timeout'],
    )
