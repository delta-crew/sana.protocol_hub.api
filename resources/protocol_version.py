import app.hooks
import falcon

from app import db
from app.constants import SUCCESS_RESPONSE, FAIL_RESPONSE
from sqlalchemy.orm import joinedload
from models import Protocol
from schemas import ProtocolSchema


@falcon.after(app.hooks.shutdown_session)
class ProtocolVersionResource(object):
    def on_get(self, req, resp, protocol_id, version_id):
        session = req.context['session']

        protocol = session.query(Protocol).\
                filter_by(Protocol.id=protocol_id, Protocol.version=version_id).\
                one()

        protocol_schema = ProtocolSchema()
        result = protocol_schema.dump(protocol)

        resp.context['result'] = result.data
