from models import OrganizationGroupMember

from marshmallow import Schema, fields, post_load


class OrganizationGroupMemberSchema(Schema):
    # TODO

    @post_load
    def make_object(self, data):
        return OrganizationMember(**data)
