from app.hooks import *
from sqlalchemy import desc
import falcon

from app import db
from app.constants import SUCCESS_RESPONSE, FAIL_RESPONSE
from models import OrganizationMDSLinkProtocol, OrganizationMDSLink, SharedProtocol
from schemas import OrganizationMDSLinkProtocolSchema


class OrganizationMDSLinkProtocolsResource(object):
    @falcon.before(login_required)
    @falcon.before(authorize_organization_user_to(OrganizationGroup.manage_mds_protocols))
    def on_get(self, req, resp, organization_id, mds_link_id):
        session = req.context['session']
        schema = OrganizationMDSLinkProtocolSchema(many=True)

        # TODO pagination?
        protocols = session.query(OrganizationMDSLinkProtocol).\
                join(OrganizationMDSLink).\
                filter(
                    OrganizationMDSLink.organization_id==organization_id,
                    OrganizationMDSLinkProtocol.mds_link_id==mds_link_id).\
                all()

        result = schema.dump(protocols)
        resp.context['result'] = result.data

    @falcon.before(login_required)
    @falcon.before(authorize_organization_user_to(OrganizationGroup.manage_mds_protocols))
    def on_post(self, req, resp, organization_id, mds_link_id):
        session = req.context['session']
        schema = OrganizationMDSLinkProtocolSchema()

        mds_link_protocol, errors = schema.load(req.context['body'], session=session)
        if errors:
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.context['type'] = FAIL_RESPONSE
            resp.context['result'] = errors
            return

        mds_link = session.query(OrganizationMDSLink).\
                filter(OrganizationMDSLink.organization_id==organization_id).\
                filter(OrganizationMDSLink.id==mds_link_id)

        if mds_link == None:
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.context['type'] = FAIL_RESPONSE
            resp.context['result'] = { 'mds_link': 'not found' }
            return

        mds_link_protocol.mds_link_id = mds_link_id

        protocol = session.query(SharedProtocol).\
                filter(SharedProtocol.protocol_id==req.context['body']['protocol_id']).\
                order_by(desc(SharedProtocol.protocol_version)).\
                first()

        if protocol == None:
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.context['type'] = FAIL_RESPONSE
            resp.context['result'] = { 'protocol': 'not found' }
            return

        mds_link_protocol.protocol = protocol.protocol
        mds_link_protocol.synchronized_version = 0

        session.add(mds_link_protocol)
        session.commit()

        result = schema.dump(mds_link_protocol)
        resp.context['result'] = result.data
