from app.hooks import *
import falcon

from app import db
from app.constants import SUCCESS_RESPONSE, FAIL_RESPONSE
from models import OrganizationMDSLinkProtocol


class OrganizationMDSLinkProtocolResource(object):
    @falcon.before(login_required)
    @falcon.before(authorize_organization_user_to(OrganizationGroup.manage_mds))
    def on_delete(self, req, res, organization_id, mds_link_id, protocol_id):
        session = req.context['session']

        mds = session.query(OrganizationMDSLinkProtocol).\
                filter_by(
                    mds_link_id=mds_link_id,
                    protocol_id=protocol_id,
                ).\
                one_or_none()

        if mds != None:
            session.delete(mds)
            session.commit()
