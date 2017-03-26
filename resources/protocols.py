from app.hooks import *
import falcon

from app import db
from app.constants import SUCCESS_RESPONSE, FAIL_RESPONSE
from sqlalchemy.orm import joinedload
from models import Protocol, SharedProtocol, OrganizationMember
from schemas import ProtocolSchema


class ProtocolsResource(object):
    @falcon.before(login_required)
    def on_get(self, req, resp):
        session = req.context['session']

        protocols = session.query(Protocol).\
                filter(Protocol.user_id==req.context['user'].id).\
                all()

        protocol_schema = ProtocolSchema(many=True)
        result = protocol_schema.dump(protocols)
        resp.context['result'] = result.data

    @falcon.before(login_required)
    def on_post(self, req, resp):
        schema = ProtocolSchema()
        session = req.context['session']
        user = req.context['user']

        protocol, errors = schema.load(req.context['body'], session=session)
        if errors:
            resp.stats = falcon.HTTP_BAD_REQUEST
            resp.context['type'] = FAIL_RESPONSE
            resp.context['result'] = errors
            return

        protocol.user = user

        session.add(protocol)
        session.commit()

        # TODO are we going to update all references to this protocol to the
        # latest version?
        if not protocol.public:
            session.query(SharedProtocol).\
                    filter(
                        SharedProtocol.protocol_id==protocol.id,
                        SharedProtocol.organization_id.in_(
                            session.query(OrganizationMember.organization_id).\
                                    filter(OrganizationMember.user_id==user.id)
                        )
                    ).\
                    update({'protocol_version': protocol.version}, synchronize_session=False)

        previous_version = protocol.previous_version(session)
        if previous_version is not None and previous_version.public:
            protocol.public = True
            session.add(protocol)
            session.commit()

        session.commit()
        result = schema.dump(protocol)
        resp.context['result'] = result.data
