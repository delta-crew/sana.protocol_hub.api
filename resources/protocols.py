from app.hooks import *
import falcon

from app import db
from app.constants import SUCCESS_RESPONSE, FAIL_RESPONSE
from sqlalchemy.orm import joinedload
from models import Protocol
from schemas import ProtocolSchema


class ProtocolsResource(object):
    @falcon.before(login_required)
    def on_get(self, req, resp, organization_id=None):
        session = req.context['session']

        if organization_id:
            protocols = session.query(SharedProtocol).\
                    options(joinedload(SharedProtocol.protocol)).\
                    filter(SharedProtocol.organization==organization_id).\
                    all()
        else:
            protocols = session.query(Protocol).\
                    filter(Protocol.user==req.context['user'].id).\
                    all()

        # TODO make sure this user is authorized to view these protocols

        protocol_schema = ProtocolSchema()
        result = protocol_schema.dump(protocol)
        resp.context['result'] = result.data

    @falcon.before(login_required)
    def on_post(self, req, res):
        # TODO how do we get the protocol and its XML from the builder...
        pass
