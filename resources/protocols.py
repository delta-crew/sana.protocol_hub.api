from app.hooks import *
import falcon

from app import db
from app.constants import SUCCESS_RESPONSE, FAIL_RESPONSE
from sqlalchemy.orm import joinedload
from models import Protocol, SharedProtocol, OrganizationMember
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
        schema = ProtocolSchema()
        session = req.context['session']
        user = resp.context['user']

        data, errors = schema.load(req.context['body'])
        if errors:
            resp.stats = falcon.HTTP_BAD_REQUEST
            resp.context['type'] = FAIL_RESPONSE
            resp.context['result'] = errors
            return

        # TODO splatting this is probably not super safe
        protocol = Protocol(**data)

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

        result = schema.dump(protocol)
        resp.conext['result'] = result.data
