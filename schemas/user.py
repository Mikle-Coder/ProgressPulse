from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from models.user import User
from core.db import Session


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        unknown = 'exclude'
        sqla_session = Session