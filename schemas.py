from models import Protocol

from marshmallow import Schema, fields, post_load


class ProtocolSchema(Schema):
    content = fields.Function(
        lambda p: p.get_content(),
        deserialize=lambda c: c)

    @post_load
    def make_object(self, data):
        return Protocol(**data)
