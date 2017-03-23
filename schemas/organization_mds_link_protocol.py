from models import OrganizationMDSLinkProtocol

from marshmallow_sqlalchemy import ModelSchema


class OrganizationMDSLinkProtocolSchema(ModelSchema):
    class Meta:
        model = OrganizationMDSLinkProtocol
