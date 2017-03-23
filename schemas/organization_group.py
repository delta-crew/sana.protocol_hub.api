from models import OrganizationGroup

from marshmallow_sqlalchemy import ModelSchema


class OrganizationGroupSchema(ModelSchema):
    class Meta:
        model = OrganizationGroup
