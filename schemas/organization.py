from models import Organization

from marshmallow_sqlalchemy import ModelSchema


class OrganizationSchema(ModelSchema):
    class Meta:
        model = Organization
