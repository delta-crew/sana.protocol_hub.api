import config

import falcon
import json

from db import Session
from models import db, Protocol
from schemas import ProtocolSchema

from wsgiref import simple_server


def shutdown_session(req, resp, resource):
    Session.remove()

class ProtocolResource(object):
    @falcon.after(shutdown_session)
    def on_get(self, req, resp, protocol_id):
        session = Session()
        protocol = session.query(Protocol).get(protocol_id)
        protocol_schema = ProtocolSchema()
        result = protocol_schema.dump(protocol)

        resp.body = json.dumps(result.data)

app = falcon.API()
protocols = ProtocolResource()
app.add_route('/protocol/{protocol_id}', protocols)
