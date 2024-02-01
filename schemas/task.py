from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.task import Task, Period, Result


class TaskSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        load_instance = True


class PeriodSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Period
        load_instance = True


class ResultSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Result
        load_instance = True