from app.hooks import *
import falcon

from app import db
from app.constants import SUCCESS_RESPONSE, FAIL_RESPONSE
from sqlalchemy.orm import joinedload
from sqlalchemy import desc
from models import Protocol, SharedProtocol, OrganizationMember
from schemas import ProtocolSchema, SharedProtocolSchema


class SharedProtocolsResource(object):
    @falcon.before(login_required)
    @falcon.before(user_belongs_to_organization)
    def on_get(self, req, resp, organization_id):
        session = req.context['session']

        protocols = session.query(Protocol).\
                join(SharedProtocol).\
                filter(SharedProtocol.organization_id==organization_id).\
                all()

        protocol_schema = ProtocolSchema(many=True)
        result = protocol_schema.dump(protocols)
        resp.context['result'] = result.data

    @falcon.before(login_required)
    @falcon.before(authorize_organization_user_to(OrganizationGroup.manage_protocols))
    def on_post(self, req, resp, organization_id):
        session = req.context['session']
        schema = SharedProtocolSchema()

        shared_protocol, errors = schema.load(req.context['body'], session=session)
        if errors:
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.context['type'] = FAIL_RESPONSE
            resp.context['result'] = errors
            return

        shared_protocol.organization_id = organization_id

        protocol = session.query(Protocol).\
            filter_by(
                id=shared_protocol.protocol.id,
                version=shared_protocol.protocol.version).\
            first()

        if protocol == None:
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.context['type'] = FAIL_RESPONSE
            resp.context['result'] = {'protocol_id': 'no protocol with id {}'.format(shared_protocol.protocol.id)}
            return

        session.add(shared_protocol)
        session.commit()

        result = schema.dump(shared_protocol)
        resp.context['result'] = result.data
