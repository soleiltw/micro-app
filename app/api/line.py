import json
import logging

import requests
from bottle import default_app

from app.api.base import BaseAPI
from app.models import LineBotSettings

app = default_app()


class Line(BaseAPI):

    def __init__(self, client_user_name=None):
        super().__init__()
        self._client_user_name = client_user_name

    def get_base_url(self):
        return app.config['line.base_url']

    def get_app_secret(self):
        lb_set = (LineBotSettings()
                  .get_by_cu(client_user_name=self._client_user_name))
        return 'Bearer ' + lb_set.channel_access_token

    def before_request(self, kwargs):
        headers = kwargs.get('headers', {})
        headers['Authorization'] = self.get_app_secret()
        headers['Content-Type'] = 'application/json'
        kwargs['headers'] = headers

    def link_line_menu(self, rich_menu_id, user_ids):
        logging.debug('user_ids: {}'.format(user_ids))
        try:
            response = self.post(
                endpoint="/v2/bot/richmenu/bulk/link",
                data=json.dumps({
                    "richMenuId": rich_menu_id,
                    "userIds": user_ids
                })
            )
            print('Response HTTP Status Code: {status_code}'.format(
                status_code=response.status_code))
            print('Response HTTP Response Body: {content}'.format(
                content=response.content))
            return response.status_code, response.content
        except requests.exceptions.RequestException:
            print('HTTP Request failed')

    def post_msg(self, user_id, msg):
        try:
            response = self.post(
                endpoint="/v2/bot/message/push",
                data=json.dumps({
                    "to": user_id,
                    "messages": [
                        {
                            "type": "text",
                            "text": msg
                        }
                    ]
                })
            )
            logging.info('Response HTTP Status Code: {status_code}'
                         .format(status_code=response.status_code))
            logging.info('Response HTTP Response Body: {content}'
                         .format(content=response.content))
        except requests.exceptions.RequestException:
            logging.error('HTTP Request failed')

    def post_with_quick_reply(self, user_id, msg, reply_items):
        try:
            response = self.post(
                endpoint="/v2/bot/message/push",
                data=json.dumps({
                    "to": user_id,
                    "messages": [
                        {
                            "type": "text",
                            "text": msg,
                            "quickReply": {
                                "items": reply_items
                            }
                        }
                    ]
                })
            )
            logging.info('Response HTTP Status Code: {status_code}'
                         .format(status_code=response.status_code))
            logging.info('Response HTTP Response Body: {content}'
                         .format(content=response.content))
        except requests.exceptions.RequestException:
            logging.error('HTTP Request failed')
