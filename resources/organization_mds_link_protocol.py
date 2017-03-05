import app.hooks
import falcon

from app import db
from app.constants import SUCCESS_RESPONSE, FAIL_RESPONSE
from models import OrganizationMDSLinkProtocol
from schemas import OrganizationMDSLinkProtocolSchema


@falcon.after(app.hooks.shutdown_session)
class OrganizationMDSLinkProtocolResource(object):
    def on_delete(self, req, res, organization_id, mds_link_id, protocol_id):
        # TODO remove organization mds link protocol
        pass
