from app.hooks import *
import falcon

from app import db
from app.constants import SUCCESS_RESPONSE, FAIL_RESPONSE
from models import Protocol
from schemas import ProtocolSchema


class ProtocolResource(object):
    @falcon.before(login_required)
    def on_get(self, req, resp, protocol_id):
        session = req.context['session']
        protocols = session.query(Protocol).filter_by(id=protocol_id)
        if protocols == None:
            resp.status = falcon.HTTP_NOT_FOUND
            resp.context['type'] = FAIL_RESPONSE
            resp.context['result'] = {
                'protocol': 'no protocol with id {}'.format(protocol_id),
            }
            return

        # TODO authorize that this user can view this protocol

        protocol_schema = ProtocolSchema(many=True)
        result = protocol_schema.dump(protocols)

        resp.context['result'] = result.data

    @falcon.before(login_required)
    def on_put(self, req, res):
        # TODO how do we get the protocol and its XML from the builder...
        schema = ProtocolSchema()
        session = req.context['session']
        user = resp.context['user']

        public = bool(req.data['public'])
        session.query(Protocol).\
                filter(Protocol.id==protocol_id).\
                update({ 'public': public })

        session.commit()

        resp.context['result'] = {}
