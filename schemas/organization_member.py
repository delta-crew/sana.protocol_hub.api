from models import OrganizationMember

from marshmallow_sqlalchemy import ModelSchema


class OrganizationMemberSchema(ModelSchema):
    class Meta:
        model = OrganizationMember
