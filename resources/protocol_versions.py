import app.hooks
import falcon

from app import db
from app.constants import SUCCESS_RESPONSE, FAIL_RESPONSE
from sqlalchemy.orm import joinedload
from models import Protocol
from schemas import ProtocolSchema


@falcon.after(app.hooks.shutdown_session)
class ProtocolVersionsResoure(object):
    def on_get(self, req, resp, protocol_id):
        session = req.context['session']

        protocol = session.query(Protocol).\
                filter_by(Protocol.id=protocol_id).\
                all()

        result = []
        for protocol in protocols:
            protocol_schema = ProtocolSchema()
            data = protocol_schema.dump(protocol).data
            result.append(data)

        resp.context['result'] = result
