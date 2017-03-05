from models import OrganizationMDSLinkProtocol

from marshmallow import Schema, fields, post_load


class OrganizationMDSLinkProtocolSchema(Schema):
    # TODO

    @post_load
    def make_object(self, data):
        return OrganizationMDSLinkProtocol(**data)
