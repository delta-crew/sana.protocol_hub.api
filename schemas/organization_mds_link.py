from models import OrganizationMDSLink

from marshmallow import Schema, fields, post_load


class OrganizationMDSLinkSchema(Schema):
    # TODO

    @post_load
    def make_object(self, data):
        return OrganizationMDSLink(**data)
