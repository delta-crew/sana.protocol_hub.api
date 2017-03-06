from app.hooks import *
import falcon

from app import db
from app.constants import SUCCESS_RESPONSE, FAIL_RESPONSE
from models import OrganizationMDSLinkProtocol
from schemas import OrganizationMDSLinkProtocolSchema


class OrganizationMDSLinkProtocolsResource(object):
    @falcon.before(login_required)
    @falcon.before(authorize_organization_user_to(OrganizationGroup.manage_mds_protocols))
    def on_get(self, req, res, organization_id, mds_link_id):
        session = req.context['session']
        schema = OrganizationMDSLinkProtocolSchema()

        # TODO pagination?
        protocols = session.query(OrganizationMDSLinkProtocol).\
                filter_by(organization_id=organization_id, mds_link_id=mds_link_id).\
                all()

        result = schema.dump(groups)
        resp.context['result'] = result.data

    @falcon.before(login_required)
    @falcon.before(authorize_organization_user_to(OrganizationGroup.manage_mds_protocols))
    def on_post(self, req, res, organization_id, mds_link_id):
        session = req.context['session']
        schema = OrganizationMDSLinkProtocolSchema()

        data, errors = schema.load(req.context['body'])
        if errors:
            resp.stats = falcon.HTTP_BAD_REQUEST
            resp.context['type'] = FAIL_RESPONSE
            resp.context['result'] = errors
            return

        protocol = OrganizationMDSLinkProtocol(
            mds_link_id=mds_link_id,
            protocol_id=data['protocol_id'],
        )
        session.add(protocol)
        session.commit()

        result = schema.dump(protocol)
        resp.conext['result'] = result.data
