from models import OrganizationMember

from marshmallow import Schema, fields, post_load


class OrganizationMemberSchema(Schema):
    # TODO

    @post_load
    def make_object(self, data):
        return OrganizationMember(**data)
