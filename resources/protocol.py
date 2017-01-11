import app.hooks
import falcon
import json

from app import db
from models import Protocol
from schemas import ProtocolSchema


class ProtocolResource(object):
    @falcon.after(app.hooks.shutdown_session)
    def on_get(self, req, resp, protocol_id):
        session = db.Session()
        protocol = session.query(Protocol).get(protocol_id)
        protocol_schema = ProtocolSchema()
        result = protocol_schema.dump(protocol)

        resp.body = json.dumps(result.data)
