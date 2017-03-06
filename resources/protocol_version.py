from app.hooks import *
import falcon

from app import db
from app.constants import SUCCESS_RESPONSE, FAIL_RESPONSE
from sqlalchemy.orm import joinedload
from models import Protocol
from schemas import ProtocolSchema


class ProtocolVersionResource(object):
    @falcon.before(login_required)
    def on_get(self, req, resp, protocol_id, version_id):
        session = req.context['session']

        protocol = session.query(Protocol).\
                filter(Protocol.id==protocol_id).\
                filter(Protocol.version==version_id).\
                one()

        # TODO make sure user is authorized to view this protocol

        protocol_schema = ProtocolSchema()
        result = protocol_schema.dump(protocol)

        resp.context['result'] = result.data
