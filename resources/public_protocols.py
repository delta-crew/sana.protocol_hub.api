import falcon
from sqlalchemy.sql import func, label

from app import db
from app.constants import SUCCESS_RESPONSE, FAIL_RESPONSE
from app.hooks import *
from sqlalchemy.orm import joinedload
from models import Protocol
from schemas import ProtocolSchema


class PublicProtocolsResource(object):
    def on_get(self, req, resp):
        session = req.context['session']
        query = req.params.get('query', '')
        protocol_schema = ProtocolSchema(many=True)

        latest_version = session.\
            query(
                label('id', Protocol.id),
                label('max_version', func.max(Protocol.version))).\
            group_by(Protocol.id).\
            subquery()
        protocols = session.query(Protocol).\
                filter(
                    Protocol.public==True,
                    Protocol.title.ilike('%' + query + '%'),
                )
        most_recent_protocols = protocols.\
            join(latest_version, Protocol.id==latest_version.c.id).\
            filter(Protocol.version==latest_version.c.max_version).\
            all()

        result = protocol_schema.dump(most_recent_protocols)
        resp.context['result'] = result.data
