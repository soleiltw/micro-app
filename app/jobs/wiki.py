import logging

from app.api.line import Line
from app.models import (
    ClientUser,
    WikiPage,
    WikiPageStatus,
    NotifyChannel,
    NotifyChannelRole
)


class WikiJob:

    def check_page_pending_review(self, client_user_name, check_count=5):
        c_u = (ClientUser.get(ClientUser.name == client_user_name))

        wps = (WikiPage
               .select(WikiPage.ask_keyword)
               .distinct()
               .where(WikiPage.status == WikiPageStatus.DRAFT.value))
        logging.debug('{} wiki keyword pending for review.'.format(len(wps)))

        if len(wps) < check_count:
            return

        line_service = Line(client_user_name=c_u.name)
        for role in NotifyChannel.filter(NotifyChannel.role ==
                                         NotifyChannelRole.REPORTER.value):
            logging.debug('Start to send to {}'.format(role.user_id))
            line_service.post_msg(role.user_id,
                                  '累積 {} 則 wiki 字詞等候審核。'
                                  .format(len(wps)))
