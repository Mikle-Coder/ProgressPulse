from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.task import Task
from core.db import Session


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        load_instance = True
        sqla_session = Session