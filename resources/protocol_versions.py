from app.hooks import *
import falcon

from app import db
from app.constants import SUCCESS_RESPONSE, FAIL_RESPONSE
from sqlalchemy.orm import joinedload
from models import Protocol
from schemas import ProtocolSchema


class ProtocolVersionsResource(object):
    @falcon.before(login_required)
    def on_get(self, req, resp, protocol_id):
        protocol_schema = ProtocolSchema()
        session = req.context['session']

        protocols = session.query(Protocol).\
                filter(Protocol.id==protocol_id).\
                all()

        # TODO make sure user is authorized to view this protocol's versions

        data = protocol_schema.dump(protocols)
        resp.context['result'] = result.data
