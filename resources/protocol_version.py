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
        protocol = session.query(Protocol).filter_by(
            id=protocol_id, version=version_id).first()
        if protocol == None:
            resp.status = falcon.HTTP_NOT_FOUND
            resp.context['type'] = FAIL_RESPONSE
            resp.context['result'] = {
                'protocol': 'no protocol with id {} and version {}'.format(
                    protocol_id, version_id),
            }
            return

        # TODO authorize that this user can view this protocol

        protocol_schema = ProtocolSchema()
        result = protocol_schema.dump(protocol)

        resp.context['result'] = result.data
