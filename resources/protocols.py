import app.hooks
import falcon

from app import db
from app.constants import SUCCESS_RESPONSE, FAIL_RESPONSE
from sqlalchemy.orm import joinedload
from models import Protocol
from schemas import ProtocolSchema


@falcon.after(app.hooks.shutdown_session)
class ProtocolsResource(object):
    def on_get(self, req, resp, organization_id=None):
        session = req.context['session']

        if organization_id:
            protocols = session.query(SharedProtocol).\
                    options(joinedload(SharedProtocol.protocol)).\
                    filter_by(SharedProtocol.organization=organization_id).\
                    all()
        else:
            protocols = session.query(Protocol).\
                    filter_by(Protocol.user=req.context['user'].id).\
                    all()

        protocol_schema = ProtocolSchema()
        result = protocol_schema.dump(protocol)
        resp.context['result'] = result.data

    def on_post(self, req, res):
        # TODO
        resp.context['result'] = { 'message': 'TODO' }
