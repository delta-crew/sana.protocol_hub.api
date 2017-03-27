from models import OrganizationMDSLink

from marshmallow_sqlalchemy import ModelSchema


class OrganizationMDSLinkSchema(ModelSchema):
    class Meta:
        exclude = ['protocols']
        model = OrganizationMDSLink
