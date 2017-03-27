from models import OrganizationMDSLinkProtocol
from schemas import ProtocolSchema

from marshmallow.fields import Nested
from marshmallow_sqlalchemy import ModelSchema


class OrganizationMDSLinkProtocolSchema(ModelSchema):
    class Meta:
        model = OrganizationMDSLinkProtocol
    protocol = Nested(ProtocolSchema)
