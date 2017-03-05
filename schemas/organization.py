from models import Organization

from marshmallow import Schema, fields, post_load


class OrganizationSchema(Schema):
    # TODO

    @post_load
    def make_object(self, data):
        return Organization(**data)
