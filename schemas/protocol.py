from models import Protocol

from marshmallow_sqlalchemy import ModelSchema


class ProtocolSchema(ModelSchema):
    class Meta:
        model = Protocol
