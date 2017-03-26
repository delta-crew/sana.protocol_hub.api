from models import OrganizationMember
from schemas import UserSchema

from marshmallow.fields import Nested
from marshmallow_sqlalchemy import ModelSchema


class OrganizationMemberSchema(ModelSchema):
    class Meta:
        model = OrganizationMember
    user = Nested(UserSchema)
