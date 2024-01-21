from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from models.telegram import Telegram
from core.db import Session


class TelegramSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Telegram
        load_instance = True
        unknown = 'exclude'
        sqla_session = Session
        exclude = ['telegram_id']

    id = fields.Integer(attribute='telegram_id')