from app.hooks import *
import falcon

from app import db
from app.constants import SUCCESS_RESPONSE, FAIL_RESPONSE
from models import Protocol
from schemas import ProtocolSchema
from sqlalchemy import desc


class ProtocolResource(object):
    @falcon.before(login_required)
    def on_get(self, req, resp, protocol_id):
        session = req.context['session']
        protocol = session.query(Protocol).\
            filter_by(id=protocol_id).\
            order_by(desc(Protocol.version)).\
            first()

        if protocol == None:
            resp.status = falcon.HTTP_NOT_FOUND
            resp.context['type'] = FAIL_RESPONSE
            resp.context['result'] = {
                'protocol': 'no protocol with id {}'.format(protocol_id),
            }
            return

        # TODO authorize that this user can view this protocol

        protocol_schema = ProtocolSchema()
        result = protocol_schema.dump(protocol)

        resp.context['result'] = result.data

    @falcon.before(login_required)
    def on_put(self, req, resp, protocol_id):
        schema = ProtocolSchema()
        session = req.context['session']

        public = bool(req.context['body']['public'])
        session.query(Protocol).\
                filter(Protocol.id==protocol_id).\
                update({ 'public': public })

        session.commit()

        resp.context['result'] = {}
