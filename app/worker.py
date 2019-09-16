import logging
import bottle

from app.sns import MessageAction

app = bottle.default_app()
actions = {}


def action(msg_action):
    action_name = msg_action.value.lower()
    if action_name not in actions:
        actions[action_name] = []

    def wrapper(func):
        actions[action_name].append(func)
        return func

    return wrapper


@action(MessageAction.HEALTH_CHECK)
def health_check(payload, msg_id):
    logging.info('payload: {}. msg_id: {}.'.format(str(payload), msg_id))
    pass
