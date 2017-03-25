from app.hooks import *
import falcon

from app import db
from app.constants import SUCCESS_RESPONSE, FAIL_RESPONSE
from sqlalchemy.orm import joinedload
from sqlalchemy import desc
from models import Protocol, SharedProtocol, OrganizationMember
from schemas import ProtocolSchema


class SharedProtocolsResource(object):
    @falcon.before(login_required)
    @falcon.before(user_belongs_to_organization)
    def on_get(self, req, resp, organization_id):
        session = req.context['session']

        protocols = session.query(SharedProtocol.protocol).\
                options(joinedload(SharedProtocol.protocol)).\
                filter(SharedProtocol.organization==organization_id).\
                all()

        protocol_schema = ProtocolSchema()
        result = protocol_schema.dump(protocol)
        resp.context['result'] = result.data

    @falcon.before(login_required)
    @falcon.before(authorize_organization_user_to(OrganizationGroup.manage_protocols))
    def on_post(self, req, resp, organization_id):
        session = req.context['session']
        user = resp.context['user']

        current = session.query(Protocol).\
                filter(id=req.data['protocolId']).\
                order_by(desc(Protocol.version)).\
                one()

        if current == None:
            resp.stats = falcon.HTTP_BAD_REQUEST
            resp.context['type'] = FAIL_RESPONSE
            resp.context['result'] = {'protocolId': 'not found'}
            return

        protocol = SharedProtocol(
            protocol_id=current.id,
            version_id=current.version,
        )

        session.add(protocol)
        session.commit()

        result = schema.dump(protocol)
        resp.conext['result'] = result.data
