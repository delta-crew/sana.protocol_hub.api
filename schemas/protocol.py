from models import Protocol

from marshmallow.fields import Nested
from marshmallow_sqlalchemy import ModelSchema


class ProtocolSchema(ModelSchema):
    class Meta:
        model = Protocol
    user = Nested(UserSchema)
