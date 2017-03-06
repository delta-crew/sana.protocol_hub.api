from app.hooks import *
import falcon

from app import db
from app.constants import SUCCESS_RESPONSE, FAIL_RESPONSE
from sqlalchemy.orm import joinedload
from models import Protocol
from schemas import ProtocolSchema


class PublicProtocolsResource(object):
    def on_get(self, req, resp, organization_id):
        session = req.context['session']

        protocols = session.query(Protocol).\
                filter(Protocol.public==True).\
                all()

        result = []
        for protocol in protocols:
            protocol_schema = ProtocolSchema()
            data = protocol_schema.dump(protocol).data
            result.append(data)

        resp.context['result'] = result
