import logging

import schedule
import time

from app.app import init_app
from app.jobs.wiki import WikiJob
from app.models import ClientUserName


def health_check():
    logging.info('Health check pass')


def wiki_pending_review():
    wiki = WikiJob()
    wiki.check_page_pending_review(ClientUserName.LISHIZHEN.value,
                                   check_count=5)


def default_run():
    logging.debug('Default run start...')
    schedule.every(1).minute.do(health_check)
    schedule.every(10).minutes.do(wiki_pending_review)
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
