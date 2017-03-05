import app.hooks
import falcon

from app import db
from app.constants import SUCCESS_RESPONSE, FAIL_RESPONSE
from models import OrganizationMDSLink


@falcon.after(app.hooks.shutdown_session)
class OrganizationMDSLinkProtocolResource(object):
    def on_post(self, req, res, organization_id, mds_link_id):
        # TODO sync all protocols in the mds link
        pass