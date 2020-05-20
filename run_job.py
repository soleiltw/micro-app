import logging

import schedule
import time

from app.app import init_app


def health_check():
    logging.info('Health check pass')


def default_run():
    logging.debug('Default run start...')
    schedule.every(1).minute.do(health_check)
    logging.info('Default run done.')


def loop():
    logging.debug('Start loop')
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == '__main__':
    init_app()
    default_run()
    loop()
