from models import OrganizationGroup

from marshmallow import Schema, fields, post_load


class OrganizationGroupSchema(Schema):
    # TODO

    @post_load
    def make_object(self, data):
        return OrganizationGroup(**data)
