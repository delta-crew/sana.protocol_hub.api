import app.hooks
import falcon

from app import db
from app.constants import SUCCESS_RESPONSE, FAIL_RESPONSE
from models import OrganizationMDSLinkProtocol
from schemas import OrganizationMDSLinkProtocolSchema


class OrganizationMDSLinkProtocolsResource(object):
    def on_get(self, req, res, organization_id, mds_link_id):
        # TODO list organization mds link protocols
        pass

    def on_post(self, req, res, organization_id, mds_link_id):
        # TODO add protocol to mds link
        pass
