from datetime import datetime

from peewee import Model, DateTimeField, BigIntegerField, CharField, SQL, \
    TextField, SmallIntegerField, IntegerField, ForeignKeyField

from app.db import db
from app.utils import ChoiceEnum


class UserChannel(ChoiceEnum):
    UNKNOWN = 0
    LINE = 1
    PINCHAT = 2
    FB_MSG = 3
    API = 4


class ModelBase(Model):
    created_at = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    updated_at = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP'),
                                            SQL('ON UPDATE CURRENT_TIMESTAMP')])

    def save(self, force_insert=False, only=None):
        self.updated_at = datetime.now()
        return super().save(force_insert, only)

    def update_dict(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        return self

    class Meta:
        database = db


class ClientUserState(ChoiceEnum):
    DEFAULT = 0
    AVAILABLE = 1
    UNAVAILABLE = 2


class APIUser(ModelBase):
    id = BigIntegerField(primary_key=True)
    name = CharField(max_length=64)
    token = CharField(max_length=64)
    expire_at = DateTimeField(null=True)

    class Meta:
        db_table = 'api_user'


class NotifyChannelRole(ChoiceEnum):
    REPORTER = 1


class NotifyChannel(ModelBase):
    id = BigIntegerField(primary_key=True)
    channel = SmallIntegerField(choices=UserChannel.choices(),
                                default=UserChannel.LINE.value)
    user_id = CharField()
    role = SmallIntegerField(choices=NotifyChannelRole.choices(),
                             default=NotifyChannelRole.REPORTER.value)

    class Meta:
        db_table = 'notify_channel'


class ClientUserName(ChoiceEnum):
    SOLEILTW = 'soleiltw'
    LISHIZHEN = 'lishizhen'


class ClientUser(ModelBase):
    id = IntegerField(primary_key=True)
    api_user = ForeignKeyField(APIUser, related_name='client_users')
    name = CharField(max_length=64)
    state = SmallIntegerField(choices=ClientUserState.choices(),
                              default=ClientUserState.DEFAULT.value)

    class Meta:
        db_table = 'client_user'


class WikiPageStatus(ChoiceEnum):
    DRAFT = 0
    USE = 1
    DROP = 2


class WikiPage(ModelBase):
    id = BigIntegerField(primary_key=True)
    status = SmallIntegerField(choices=WikiPageStatus.choices(),
                               default=WikiPageStatus.DRAFT.value)
    title = CharField(max_length=255)
    alt_title = CharField(max_length=255)
    summary = TextField()
    content = TextField()
    url = TextField()
    links = TextField()
    ask_keyword = CharField(max_length=255)

    class Meta:
        db_table = 'wiki_page'


class LineBotSettings(ModelBase):
    id = BigIntegerField(primary_key=True)
    client_user = ForeignKeyField(ClientUser, related_name='line_bot_st_cus')
    channel_access_token = CharField(max_length=255)
    channel_secret = CharField(max_length=64)

    def get_by_cu(self, client_user_name):
        cu = ClientUser.get(name=client_user_name)
        return self.get(client_user=cu)

    def get_by_cuo(self, cu):
        return self.get(client_user=cu)

    class Meta:
        db_table = 'line_bot_settings'
