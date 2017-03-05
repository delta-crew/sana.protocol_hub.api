import app.hooks
import falcon

from app import db
from app.constants import SUCCESS_RESPONSE, FAIL_RESPONSE
from models import OrganizationMember


class OrganizationMemberResource(object):
    def on_delete(self, req, res, organization_id, group_id, member_id):
        # TODO remove organization group member
        pass
