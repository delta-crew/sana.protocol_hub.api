from app.hooks import *
import falcon

from app import db
from app.constants import SUCCESS_RESPONSE, FAIL_RESPONSE
from models import OrganizationMDSLink, OrganizationMDSLinkProtocol


class OrganizationMDSLinkProtocolResource(object):
    @falcon.before(login_required)
    @falcon.before(authorize_organization_user_to(OrganizationGroup.manage_mds))
    def on_delete(self, req, resp, organization_id, mds_link_id, protocol_id):
        session = req.context['session']

        mds_link_protocol = session.query(OrganizationMDSLinkProtocol).\
                join(OrganizationMDSLink).\
                filter(
                    OrganizationMDSLink.organization_id==organization_id,
                    OrganizationMDSLinkProtocol.protocol_id==protocol_id,
                    OrganizationMDSLinkProtocol.mds_link_id==mds_link_id).\
                first()

        if mds_link_protocol == None:
            resp.status = falcon.HTTP_NOT_FOUND
            resp.context['type'] = FAIL_RESPONSE
            resp.context['result'] = {
                'group': 'no mds link with id {}'.format(mds_link_id),
            }
            return

        session.delete(mds_link_protocol)
        session.commit()
        resp.context['result'] = {}
