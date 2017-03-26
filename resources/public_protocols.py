from app.hooks import *
import falcon

from app import db
from app.constants import SUCCESS_RESPONSE, FAIL_RESPONSE
from sqlalchemy.orm import joinedload
from models import Protocol
from schemas import ProtocolSchema


class PublicProtocolsResource(object):
    def on_get(self, req, resp):
        session = req.context['session']
        query = req.params.get('query', '')
        protocol_schema = ProtocolSchema(many=True)

        protocols = session.query(Protocol).\
                filter(
                    Protocol.public==True,
                    Protocol.title.ilike('%' + query + '%'),
                ).\
                all()

        result = protocol_schema.dump(protocols)
        resp.context['result'] = result.data
