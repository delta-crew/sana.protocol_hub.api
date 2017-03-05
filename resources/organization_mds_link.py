import app.hooks
import falcon

from app import db
from app.constants import SUCCESS_RESPONSE, FAIL_RESPONSE
from models import OrganizationMDSLink
from schemas import OrganizationMDSLinkSchema


@falcon.after(app.hooks.shutdown_session)
class OrganizationMDSLinkResource(object):
    def on_get(self, req, res, organization_id, mds_link_id):
        # TODO get organization mds link
        pass

    def on_delete(self, req, res, organization_id, mds_link_id):
        # TODO remove organization mds link
        pass
