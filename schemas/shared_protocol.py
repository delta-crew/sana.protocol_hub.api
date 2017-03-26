from models import SharedProtocol

from marshmallow_sqlalchemy import ModelSchema


class SharedProtocolSchema(ModelSchema):
    class Meta:
        model = SharedProtocol
