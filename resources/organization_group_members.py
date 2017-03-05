import app.hooks
import falcon

from app import db
from app.constants import SUCCESS_RESPONSE, FAIL_RESPONSE
from models import OrganizationGroupMember
from schemas import OrganizationGroupMemberSchema


@falcon.after(app.hooks.shutdown_session)
class OrganizationGroupMembersResource(object):
    def on_get(self, req, res, organization_id, group_id):
        # TODO list organization group members
        pass

    def on_post(self, req, res, organization_id, group_id):
        # TODO add organization group member
        pass
