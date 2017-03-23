from models import OrganizationGroupMember

from marshmallow_sqlalchemy import ModelSchema


class OrganizationGroupMemberSchema(ModelSchema):
    class Meta:
        model = OrganizationGroupMember
