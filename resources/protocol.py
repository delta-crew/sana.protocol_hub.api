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
        protocol = session.query(Protocol).get(protocol_id)
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
    def on_put(self, req, res):
        # TODO how do we get the protocol and its XML from the builder...
        schema = ProtocolSchema()
        session = req.context['session']
        user = resp.context['user']

        # TODO splatting this is probably not super safe
        protocol = session.query(Protocol).get(protocol_id)

        protocol.public = bool(req.data['public'])

        session.add(protocol)
        session.commit()

        # TODO are we going to update all references to this protocol to the
        # latest version?
        if protocol.public:
            session.query(SharedProtocol).\
                    filter(
                            SharedProtocol.protocol_id==protocol.id,
                            SharedProtocol.organization_id.in_(
                                session.query(OrganizationMember.organization_id).\
                                        filter(OrganizationMember.member_id==user.id)
                            )
                    ).\
                    update({'synchronized_version': protocol.version})
            session.commit()

        protocol_schema = ProtocolSchema()
        result = protocol_schema.dump(protocol)

        resp.context['result'] = result.data
